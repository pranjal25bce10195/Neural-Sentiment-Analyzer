
import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from logic import get_mood, Mood

# Neon Palette 
BG_DEEP     = "#05060F"   # near-black space bg
BG_PANEL    = "#0D0F1E"   # slightly lighter panel
BG_INPUT    = "#0A0B18"   # input field bg
BORDER_DIM  = "#1A1D3A"   # subtle border
BORDER_GLOW = "#1F2450"   # glowing border

NEON_CYAN   = "#00F5FF"
NEON_PINK   = "#FF2D78"
NEON_GREEN  = "#39FF14"
NEON_PURPLE = "#BF5FFF"
NEON_AMBER  = "#FFB800"

TEXT_MAIN   = "#E8EAFF"
TEXT_DIM    = "#5A5F8A"
TEXT_MUTED  = "#2E3260"

FONT_MONO   = ("Consolas", 11)
FONT_TITLE  = ("Consolas", 22, "bold")
FONT_LABEL  = ("Consolas", 10)
FONT_SMALL  = ("Consolas", 9)
FONT_SCORE  = ("Consolas", 36, "bold")
FONT_CAT    = ("Consolas", 14, "bold")
FONT_BADGE  = ("Consolas", 9, "bold")


class NeonButton(tk.Canvas):
    """Animated neon-glowing button rendered on Canvas."""
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, bg=BG_DEEP, bd=0, highlightthickness=0,
                         cursor="hand2", **kwargs)
        self._text = text
        self._cmd  = command
        self._hovered = False
        self.bind("<Configure>", self._draw)
        self.bind("<Enter>",     self._on_enter)
        self.bind("<Leave>",     self._on_leave)
        self.bind("<Button-1>",  self._on_click)

    def _draw(self, _=None):
        self.delete("all")
        w = self.winfo_width() or int(self["width"])
        h = self.winfo_height() or int(self["height"])
        pad = 2
        color  = NEON_CYAN if self._hovered else NEON_PURPLE
        fill   = "#0A1530" if self._hovered else BG_PANEL
        # outer glow rect
        self.create_rectangle(pad, pad, w-pad, h-pad,
                               outline=color, fill=fill, width=2)
        # inner faint rect
        self.create_rectangle(pad+3, pad+3, w-pad-3, h-pad-3,
                               outline=self._dim(color), fill="", width=1)
        # label
        self.create_text(w//2, h//2, text=self._text,
                         font=("Consolas", 11, "bold"),
                         fill=color)

    def _dim(self, hex_color):
        r = int(hex_color[1:3], 16) // 3
        g = int(hex_color[3:5], 16) // 3
        b = int(hex_color[5:7], 16) // 3
        return f"#{r:02x}{g:02x}{b:02x}"

    def _on_enter(self, _):
        self._hovered = True
        self._draw()

    def _on_leave(self, _):
        self._hovered = False
        self._draw()

    def _on_click(self, _):
        self._cmd()


class ConfidenceBar(tk.Canvas):
    """Custom neon progress bar."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BG_PANEL, bd=0,
                         highlightthickness=0, **kwargs)
        self._value = 0.0
        self._color = NEON_CYAN
        self.bind("<Configure>", self._draw)

    def set(self, value, color=NEON_CYAN):
        self._value = max(0.0, min(1.0, value))
        self._color = color
        self._draw()

    def _draw(self, _=None):
        self.delete("all")
        w = self.winfo_width() or int(self["width"])
        h = self.winfo_height() or int(self["height"])
        # track
        self.create_rectangle(0, 0, w, h, fill=BORDER_DIM, outline="")
        # fill
        if self._value > 0:
            fw = int((w - 4) * self._value)
            self.create_rectangle(2, 2, fw+2, h-2, fill=self._color, outline="")
        # tick marks
        for i in range(1, 10):
            x = int(w * i / 10)
            self.create_line(x, h-5, x, h, fill=TEXT_MUTED, width=1)


class SentimentAnalyzerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SENTIMENT ANALYZER //  AI-ML EDITION")
        self.root.geometry("680x760")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DEEP)
        self._history: list[tuple[str, Mood]] = []

        self._build_ui()
        self.root.bind("<Control-Return>", lambda _: self.analyze())

    #  Build 

    def _build_ui(self):
        outer = tk.Frame(self.root, bg=BG_DEEP)
        outer.pack(fill="both", expand=True, padx=18, pady=14)

        # ── Header bar ──
        header = tk.Frame(outer, bg=BG_DEEP)
        header.pack(fill="x", pady=(0, 10))

        tk.Label(header, text="NEURAL", font=("Consolas", 24, "bold"),
                 bg=BG_DEEP, fg=NEON_CYAN).pack(side="left")
        tk.Label(header, text="SENTIMENT", font=("Consolas", 24, "bold"),
                 bg=BG_DEEP, fg=NEON_PINK).pack(side="left")

        badge_frame = tk.Frame(header, bg=NEON_PURPLE, padx=6, pady=2)
        badge_frame.pack(side="right", pady=10)
        tk.Label(badge_frame, text="ML EDITION", font=FONT_BADGE,
                 bg=NEON_PURPLE, fg=BG_DEEP).pack()

        # horizontal rule
        tk.Frame(outer, bg=BORDER_GLOW, height=1).pack(fill="x", pady=(0, 14))

        # ── Input panel ──
        input_panel = tk.Frame(outer, bg=BG_PANEL, padx=14, pady=12)
        input_panel.pack(fill="x")
        input_panel.config(relief="flat", bd=0)

        tk.Label(input_panel, text="// INPUT TEXT",
                 font=FONT_LABEL, bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w")

        # text area with neon border
        ta_wrapper = tk.Frame(input_panel, bg=NEON_PURPLE, padx=1, pady=1)
        ta_wrapper.pack(fill="x", pady=(6, 0))
        ta_inner = tk.Frame(ta_wrapper, bg=BG_INPUT)
        ta_inner.pack(fill="x")

        self.text_input = tk.Text(
            ta_inner, wrap="word", height=7,
            font=FONT_MONO, bg=BG_INPUT, fg=TEXT_MAIN,
            insertbackground=NEON_CYAN,
            selectbackground=NEON_PURPLE, selectforeground=BG_DEEP,
            relief="flat", bd=6, cursor="xterm")
        self.text_input.pack(fill="x")
        self.text_input.bind("<KeyRelease>", self._on_keyrelease)

        # char counter
        self.char_var = tk.StringVar(value="0 chars")
        tk.Label(input_panel, textvariable=self.char_var,
                 font=FONT_SMALL, bg=BG_PANEL, fg=TEXT_DIM,
                 anchor="e").pack(fill="x")

        # ── Threshold row ──
        thr_panel = tk.Frame(outer, bg=BG_DEEP, pady=10)
        thr_panel.pack(fill="x")

        tk.Label(thr_panel, text="SENSITIVITY THRESHOLD",
                 font=FONT_LABEL, bg=BG_DEEP, fg=TEXT_DIM).pack(side="left")

        self.threshold_var = tk.DoubleVar(value=0.15)
        slider = ttk.Scale(thr_panel, from_=0.1, to=0.9, orient="horizontal",
                           variable=self.threshold_var, length=260,
                           command=self._on_slider)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Horizontal.TScale",
                        background=BG_DEEP,
                        troughcolor=BORDER_DIM,
                        sliderthickness=14,
                        sliderrelief="flat")
        slider.configure(style="Custom.Horizontal.TScale")
        slider.pack(side="left", padx=12)

        self.thr_label = tk.Label(thr_panel, text="0.15",
                                  font=("Consolas", 10, "bold"),
                                  bg=BG_DEEP, fg=NEON_AMBER, width=5)
        self.thr_label.pack(side="left")

        # ── Analyze button ──
        btn = NeonButton(outer, text="  ANALYZE SENTIMENT  ─▶",
                         command=self.analyze, width=300, height=44)
        btn.pack(pady=10)

        # ── Result panel ──
        result_frame = tk.Frame(outer, bg=BG_PANEL, padx=16, pady=14)
        result_frame.pack(fill="x")
        tk.Label(result_frame, text="// ANALYSIS OUTPUT",
                 font=FONT_LABEL, bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w")

        # emoji + category row
        disp_row = tk.Frame(result_frame, bg=BG_PANEL)
        disp_row.pack(fill="x", pady=(8, 0))

        self.emoji_label = tk.Label(disp_row, text="◈",
                                    font=("Consolas", 40),
                                    bg=BG_PANEL, fg=TEXT_MUTED)
        self.emoji_label.pack(side="left")

        info_col = tk.Frame(disp_row, bg=BG_PANEL)
        info_col.pack(side="left", padx=14)

        self.cat_label = tk.Label(info_col, text="AWAITING INPUT",
                                  font=FONT_CAT, bg=BG_PANEL, fg=TEXT_DIM)
        self.cat_label.pack(anchor="w")

        self.score_label = tk.Label(info_col, text="score: ─────",
                                    font=("Consolas", 11),
                                    bg=BG_PANEL, fg=TEXT_DIM)
        self.score_label.pack(anchor="w", pady=2)

        self.method_label = tk.Label(info_col, text="",
                                     font=FONT_SMALL,
                                     bg=BG_PANEL, fg=TEXT_DIM)
        self.method_label.pack(anchor="w")

        # confidence bar
        tk.Frame(result_frame, bg=BORDER_DIM, height=1).pack(fill="x", pady=8)

        conf_row = tk.Frame(result_frame, bg=BG_PANEL)
        conf_row.pack(fill="x")
        tk.Label(conf_row, text="MODEL CONFIDENCE",
                 font=FONT_SMALL, bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w")

        self.conf_pct = tk.Label(conf_row, text="",
                                 font=("Consolas", 10, "bold"),
                                 bg=BG_PANEL, fg=NEON_CYAN, anchor="e")
        self.conf_pct.pack(fill="x")

        self.conf_bar = ConfidenceBar(result_frame, height=10)
        self.conf_bar.pack(fill="x", pady=(4, 0))

        # ── History panel ──
        tk.Frame(outer, bg=BORDER_GLOW, height=1).pack(fill="x", pady=(14, 4))
        tk.Label(outer, text="// RECENT ANALYSES",
                 font=FONT_LABEL, bg=BG_DEEP, fg=TEXT_DIM).pack(anchor="w")

        self.history_frame = tk.Frame(outer, bg=BG_DEEP)
        self.history_frame.pack(fill="x", pady=(4, 0))

        # ── Footer ──
        tk.Frame(outer, bg=BORDER_DIM, height=1).pack(fill="x", pady=(12, 4))
        footer = tk.Frame(outer, bg=BG_DEEP)
        footer.pack(fill="x")
        tk.Label(footer, text="CTRL+ENTER  ·  ANALYZE",
                 font=FONT_SMALL, bg=BG_DEEP, fg=TEXT_MUTED).pack(side="left")
        tk.Label(footer, text="LOGISTIC REGRESSION  +  TF-IDF",
                 font=FONT_SMALL, bg=BG_DEEP, fg=TEXT_MUTED).pack(side="right")

    #  Callbacks

    def _on_slider(self, value):
        self.thr_label.config(text=f"{float(value):.2f}")

    def _on_keyrelease(self, _=None):
        n = len(self.text_input.get("1.0", "end-1c"))
        self.char_var.set(f"{n} chars")

    def analyze(self):
        text = self.text_input.get("1.0", "end-1c").strip()
        if not text:
            self._flash_error()
            return

        threshold = self.threshold_var.get()
        mood      = get_mood(text, threshold=threshold)
        self._history.append((text, mood))
        self._render_result(mood, threshold)
        self._refresh_history()

    def _flash_error(self):
        self.cat_label.config(text="NO INPUT DETECTED", fg=NEON_PINK)
        self.emoji_label.config(text="⚠", fg=NEON_PINK)
        self.score_label.config(text="enter text to analyze", fg=TEXT_DIM)
        self.method_label.config(text="")
        self.conf_pct.config(text="")
        self.conf_bar.set(0)

    def _render_result(self, mood: Mood, threshold: float):
        if mood.sentiment >= threshold:
            category, neon = "POSITIVE", NEON_GREEN
        elif mood.sentiment <= -threshold:
            category, neon = "NEGATIVE", NEON_PINK
        else:
            category, neon = "NEUTRAL", NEON_AMBER

        emoji_map = {"😊": "◉ POS", "😠": "◉ NEG", "😐": "◉ NEU"}
        display_emoji = mood.emoji

        self.emoji_label.config(text=display_emoji, fg=neon)
        self.cat_label.config(text=category, fg=neon)
        sign = "+" if mood.sentiment >= 0 else ""
        self.score_label.config(
            text=f"score: {sign}{mood.sentiment:.4f}", fg=TEXT_MAIN)

        if mood.method == "ml":
            pct = mood.confidence * 100
            self.method_label.config(
                text=f"[ML]  logistic regression + tfidf", fg=NEON_PURPLE)
            self.conf_pct.config(text=f"{pct:.1f}%", fg=neon)
            self.conf_bar.set(mood.confidence, color=neon)
        else:
            self.method_label.config(
                text="[TEXTBLOB]  rule-based fallback", fg=NEON_AMBER)
            self.conf_pct.config(text="N/A", fg=TEXT_DIM)
            self.conf_bar.set(0)

    def _refresh_history(self):
        for w in self.history_frame.winfo_children():
            w.destroy()

        threshold = self.threshold_var.get()
        recent    = self._history[-5:][::-1]

        for i, (snippet, mood) in enumerate(recent):
            if mood.sentiment >= threshold:
                color = NEON_GREEN
            elif mood.sentiment <= -threshold:
                color = NEON_PINK
            else:
                color = NEON_AMBER

            row = tk.Frame(self.history_frame, bg=BG_DEEP)
            row.pack(fill="x", pady=1)

            # index badge
            badge = tk.Frame(row, bg=BORDER_DIM, padx=4, pady=1)
            badge.pack(side="left", padx=(0, 6))
            tk.Label(badge, text=f"{i+1:02d}",
                     font=FONT_SMALL, bg=BORDER_DIM, fg=TEXT_DIM).pack()

            # color dot
            dot = tk.Canvas(row, width=8, height=8, bg=BG_DEEP,
                            bd=0, highlightthickness=0)
            dot.pack(side="left", padx=(0, 6), pady=4)
            dot.create_oval(0, 0, 7, 7, fill=color, outline="")

            # snippet
            short = snippet[:60] + ("…" if len(snippet) > 60 else "")
            tk.Label(row, text=short,
                     font=FONT_SMALL, bg=BG_DEEP, fg=TEXT_DIM,
                     anchor="w").pack(side="left", fill="x", expand=True)

            # score
            sign = "+" if mood.sentiment >= 0 else ""
            tk.Label(row, text=f"{sign}{mood.sentiment:.3f}",
                     font=("Consolas", 9, "bold"),
                     bg=BG_DEEP, fg=color).pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    app  = SentimentAnalyzerGUI(root)
    root.mainloop()
