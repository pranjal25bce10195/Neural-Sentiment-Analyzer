
import os
import pickle
from dataclasses import dataclass, field
from textblob import TextBlob

# ── Paths ─────────────────────────────────────────────────────────────────────
_BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH   = os.path.join(_BASE_DIR, "models", "sentiment_model.pkl")
_ENCODER_PATH = os.path.join(_BASE_DIR, "models", "label_encoder.pkl")

# ── Blend weights ─────────────────────────────────────────────────────────────
_W_ML_DEFAULT = 0.55   # ML weight when both signals are moderate
_W_TB_DEFAULT = 0.45   # TextBlob weight when both signals are moderate
_W_TB_STRONG  = 0.75   # TextBlob weight when ML is weak but TextBlob is clear

# ── Lazy-load ML artefacts once ───────────────────────────────────────────────
_pipeline      = None
_label_encoder = None
_ml_available  = False


def _load_ml_model() -> bool:
    """Attempt to load the trained pipeline + encoder (once)."""
    global _pipeline, _label_encoder, _ml_available
    if _ml_available:
        return True
    try:
        with open(_MODEL_PATH,    "rb") as f: _pipeline      = pickle.load(f)
        with open(_ENCODER_PATH,  "rb") as f: _label_encoder = pickle.load(f)
        _ml_available = True
    except FileNotFoundError:
        _ml_available = False
    return _ml_available


# ── Data class ────────────────────────────────────────────────────────────────
@dataclass
class Mood:
    emoji:      str
    sentiment:  float
    method:     str   = field(default="textblob")   # "hybrid", "ml", or "textblob"
    confidence: float = field(default=0.0)           # ML max-prob (0 if pure TextBlob)


# ── Pre-processing (mirrors train_model.py) ───────────────────────────────────
def _preprocess(text: str) -> str:
    """Lowercase + remove stopwords for the ML pipeline.
    Intensifiers ('very', 'really', etc.) are stopwords and are stripped here —
    that is intentional for the TF-IDF model.  TextBlob sees the raw text and
    handles intensifiers correctly in the blend step.
    """
    try:
        from nltk.corpus import stopwords
        _stop  = set(stopwords.words("english"))
        tokens = text.lower().split()
        return " ".join(t for t in tokens if t.isalpha() and t not in _stop)
    except Exception:
        return text.lower()


# ── Raw ML score ──────────────────────────────────────────────────────────────
def _ml_raw(text: str) -> tuple[float, float]:
    """
    Returns (polarity, confidence).
    polarity = p_pos - p_neg ∈ (-1, 1)
    confidence = max(p_pos, p_neg)
    """
    processed  = _preprocess(text)
    proba      = _pipeline.predict_proba([processed])[0]
    classes    = list(_label_encoder.classes_)          # ['neg', 'pos']
    p_pos      = proba[classes.index("pos")]
    p_neg      = proba[classes.index("neg")]
    polarity   = p_pos - p_neg
    confidence = max(p_pos, p_neg)
    return polarity, confidence


# ── Hybrid scoring ────────────────────────────────────────────────────────────
def _hybrid_sentiment(text: str) -> tuple[float, float]:
    """
    Blend ML polarity with TextBlob polarity.

    When the ML model is uncertain about an everyday phrase (|ml| < 0.15)
    but TextBlob detects a clear emotion (|tb| > 0.4), we trust TextBlob
    more — this correctly handles sentences like 'I am very very happy'
    whose vocabulary falls outside the movie-review training domain.
    """
    ml_score, confidence = _ml_raw(text)
    tb_score = float(TextBlob(text).sentiment.polarity)

    ml_weak = abs(ml_score) < 0.15
    tb_strong = abs(tb_score) > 0.40

    if ml_weak and tb_strong:
        # Out-of-domain sentence: trust TextBlob heavily
        w_tb = _W_TB_STRONG
        w_ml = 1.0 - w_tb
    else:
        w_ml = _W_ML_DEFAULT
        w_tb = _W_TB_DEFAULT

    blended = w_ml * ml_score + w_tb * tb_score
    # Clamp to [-1, 1]
    blended = max(-1.0, min(1.0, blended))
    return blended, confidence


# ── Public API ────────────────────────────────────────────────────────────────
def get_mood(input_text: str, *, threshold: float) -> Mood:
    """
    Analyse *input_text* and return a Mood.

    Uses hybrid scoring (ML + TextBlob blend) when the model is available;
    falls back to pure TextBlob otherwise.
    """
    if _load_ml_model():
        sentiment, confidence = _hybrid_sentiment(input_text)
        method = "hybrid"
    else:
        sentiment  = float(TextBlob(input_text).sentiment.polarity)
        confidence = 0.0
        method     = "textblob"

    if sentiment >= threshold:
        emoji = "😊"
    elif sentiment <= -threshold:
        emoji = "😠"
    else:
        emoji = "😐"

    return Mood(emoji=emoji, sentiment=sentiment,
                method=method, confidence=confidence)


# ── Quick CLI test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        "I am very very happy",
        "This is absolutely terrible and I hate it",
        "The weather is okay today",
        "I love this movie so much!",
        "I feel really sad and disappointed",
    ]
    print("── Self-test ─────────────────────────────────────────────")
    for t in tests:
        mood = get_mood(t, threshold=0.15)
        tag  = f"[{mood.method}  conf={mood.confidence:.2f}]"
        print(f"  {mood.emoji}  {mood.sentiment:+.3f}  {tag}  →  {t}")
    print()

    print("── Interactive ───────────────────────────────────────────")
    while True:
        text = input("Text (Ctrl-C to quit): ").strip()
        if not text:
            continue
        mood = get_mood(text, threshold=0.15)
        tag  = f"[{mood.method}  conf={mood.confidence:.2f}]"
        print(f"  {mood.emoji}  Sentiment: {mood.sentiment:+.3f}  {tag}\n")
