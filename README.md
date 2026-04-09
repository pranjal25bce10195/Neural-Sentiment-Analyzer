# Neural Sentiment Analyzer // AI-ML Edition

## Overview

The **Neural Sentiment Analyzer** is an AI-powered desktop application that analyzes the emotional tone of text using Natural Language Processing (NLP) and Machine Learning techniques.

This project implements a **hybrid sentiment analysis system** that combines:

* Logistic Regression (Machine Learning)
* TF-IDF Vectorization
* TextBlob (rule-based NLP fallback)

The system classifies text as **Positive , Negative , or Neutral**, and provides a confidence score along with a visually rich GUI.


## Features

* Real-time sentiment analysis
* Hybrid AI model (ML + TextBlob fallback)
* Confidence score visualization
* Adjustable sensitivity threshold
* Advanced Neon-themed GUI (Tkinter)
* Recent analysis history
* Keyboard shortcut support (Ctrl + Enter)
* Fast and local processing (no internet required)


## AI/ML Concepts Used

* Supervised Learning (Logistic Regression)
* Natural Language Processing (NLP)
* TF-IDF Vectorization
* Probability-based classification (`predict_proba`)
* Hybrid intelligent system design


## Project Structure

```
project-folder/
│
├── gui.py / project.py        # GUI Application
├── logic.py                  # Sentiment Analysis Logic
├── train_model.py            # Model Training Script
├── models/
│   ├── sentiment_model.pkl
│   └── label_encoder.pkl
├── requirements.txt
└── README.md
```


## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Train the Model (IMPORTANT)

```bash
python train_model.py
```

This will create:

```
models/sentiment_model.pkl
models/label_encoder.pkl
```

---

### 3. Run the Application

```bash
python project.py
```


## How It Works

1. Input text is preprocessed (lowercasing, stopword removal)
2. TF-IDF converts text into numerical features
3. Logistic Regression predicts sentiment probability
4. TextBlob computes polarity score
5. Hybrid logic combines both results for better accuracy
6. Output is displayed with emoji, score, and confidence


## Output Example

| Input Text         | Output      |
| ------------------ | ----------- |
| "I love this!"     | 😊 Positive |
| "This is terrible" | 😠 Negative |
| "It is okay"       | 😐 Neutral  |


## Notes

* GUI works best on local system (PyCharm / terminal)
* Model must be trained before running GUI
* Works offline after setup

## Author

PRANJAL SHAHI
25BCE10195

## Future Improvements

* Multi-language sentiment analysis
* Deep learning models (LSTM / BERT)
* Web or mobile version
* Emotion detection beyond polarity


## Dataset

* NLTK `movie_reviews` dataset used for training


## Conclusion

This project demonstrates the practical application of AI and Machine Learning in solving real-world problems through an intuitive and user-friendly interface.

---
