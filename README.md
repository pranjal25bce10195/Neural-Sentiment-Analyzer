#  Sentiment Analysis Tool

A simple yet powerful Python application that analyzes the sentiment of text using Natural Language Processing (NLP) and displays results through an intuitive graphical user interface.

##  Overview

This project uses TextBlob to perform sentiment analysis on user-provided text and categorizes it as Positive, Negative, or Neutral. The application features a clean GUI built with Tkinter that makes sentiment analysis accessible to everyone.
Logic of the Program
<img width="1075" height="883" alt="image" src="https://github.com/user-attachments/assets/d46bfdfb-90eb-4b5e-b58b-c1000a9fab0d" />



##  Features

- **Real-time Sentiment Analysis**: Instantly analyze any text input
- **Visual Feedback**: Emoji-based sentiment representation 
- **Adjustable Sensitivity:** Customize threshold levels (0.1 - 0.9) for sentiment classification
- **Sentiment Score:** Displays precise polarity score (-1.0 to +1.0)
- **Color-Coded Results:**

🟢 Green for Positive sentiment
🔴 Red for Negative sentiment
⚫ Gray for Neutral sentiment

- **User-Friendly Interface:** Clean, modern GUI with scrollable text input
- 
##  Technologies Used

- **Python 3.x**
- **TextBlob**: For sentiment analysis and NLP processing
- **Tkinter**: For GUI development
- **Dataclasses**: For structured data management

##  Installation

### Prerequisites

Make sure you have Python 3.7 or higher installed on your system.

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/yourusername/sentiment-analysis-tool.git
cd sentiment-analysis-tool
```

### Step 2: Install Required Dependencies

```bash
pip install textblob
```

### Step 3: Download TextBlob Corpora (First-time setup)

```bash
python -m textblob.download_corpora
```

##  Usage

### Running the Application

Navigate to the project directory and run:

```bash
python sentiment_gui.py
```

### How to Use

1. **Enter Text**: Type or paste your text into the input box
2. **Analyze**: Click "Analyze Sentiment" button or press `Ctrl + Enter`
3. **View Results**: See the emoji and category

### Example Inputs

**Positive Sentiment:**
```
"I absolutely love this product! It exceeded all my expectations."
```
<img width="740" height="655" alt="Screenshot 2025-11-25 162252" src="https://github.com/user-attachments/assets/92a12f51-d3e0-493e-8f37-6e001cf1e886" />


**Negative Sentiment:**
```
"This is terrible. I'm very disappointed with the quality."
```
<img width="741" height="659" alt="Screenshot 2025-11-25 162342" src="https://github.com/user-attachments/assets/e94a1451-e9a7-4f40-9c68-af2c896e69e6" />



**Neutral Sentiment:**
```
"The package arrived on Tuesday. It contains three items."
```
<img width="746" height="656" alt="Screenshot 2025-11-25 162159" src="https://github.com/user-attachments/assets/10a34391-a28b-42ce-963c-cc0c5b24b7d7" />



##  Project Structure

```
sentiment-analysis-tool/
│
├── sentiment_gui.py          # Main application file with GUI
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies (optional)
```
## 📊 Understanding Sentiment Scores

Score Range: -1.0 (most negative) to +1.0 (most positive)
Positive: Score ≥ threshold
Neutral: Score between -threshold and threshold
Negative: Score ≤ -threshold

---
Default threshold is set to 0.3, which balances sensitivity and accuracy.


##  Use Cases

- **Social Media Monitoring**: Analyze customer feedback and comments
- **Product Reviews**: Understand customer satisfaction levels
- **Email Classification**: Filter and prioritize messages
- **Content Moderation**: Detect potentially harmful or negative content
- **Market Research**: Analyze survey responses and feedback
- **Customer Support**: Prioritize urgent or dissatisfied customer messages

##  Customization

### Changing Default Threshold

In `gui.py`, modify line:
```python
self.threshold_var = tk.DoubleVar(value=0.3)  # Change 0.3 to your preferred value
```

### Modifying Emojis

In the `get_mood()` function:
```python
if sentiment >= friendly_threshold:
    return Mood("😊", sentiment)  # Change to any emoji you prefer
```

### Adjusting Window Size

```python
self.root.geometry("600x500")  # Modify width x height
```

##  What can be Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'textblob'"
**Solution**: Install TextBlob
```bash
pip install textblob
```

### Issue: "LookupError: Resource punkt not found"
**Solution**: Download NLTK data
```bash
python -m textblob.download_corpora
```

### Issue: GUI doesn't appear or crashes
**Solution**: Ensure Tkinter is installed (usually comes with Python)
- On Ubuntu/Debian: `sudo apt-get install python3-tk`
- On macOS: Tkinter should be pre-installed
- On Windows: Reinstall Python with Tkinter option checked


## Future Enhancements

- [ ] Add support for multiple languages
- [ ] Save analysis history to CSV/JSON
- [ ] Batch processing for multiple texts
- [ ] Integration with social media APIs
- [ ] Export results as reports
- [ ] Advanced visualization with graphs
- [ ] Machine learning model training option

---

**Made By**
PRANJAL SHAHI
25BCE10195
