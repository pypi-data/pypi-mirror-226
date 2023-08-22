## AlienDev Sentiment Analyzer

AlienDev Sentiment Analyzer is a Python library that allows you to analyze the sentiment of textual content. This library makes use of the Google Translator API for translation and the VADER Sentiment Analysis tool for sentiment analysis.

### Installation

You can install AlienDev Sentiment Analyzer using pip:

```bash
pip install aliendev-sentiment
```

### Usage

Here's an example of how to use AlienDev Sentiment Analyzer:

```python
from aliendev_sentiment import SentimentAnalyzer

# Define the content dictionary
content = {
    "content": "..."  # Your content goes here
}

# Create a SentimentAnalyzer instance
sentiment = SentimentAnalyzer(content=content.get("content"))

# Analyze sentiment
response = sentiment.analyze_sentiment()

print("Sentiment:", response)
```

Replace the `"..."` placeholder in the `content` dictionary with your actual textual content that you want to analyze for sentiment.

### Output

The `analyze_sentiment` method of the `SentimentAnalyzer` class will return a sentiment label, which could be one of the following:
- "Positive"
- "Neutral"
- "Negative"

### Disclaimer

This library is intended for educational and informational purposes only. The sentiment analysis results provided are based on algorithms and may not accurately reflect human sentiment. Decision-making based on the sentiment analysis results should be done with caution.

