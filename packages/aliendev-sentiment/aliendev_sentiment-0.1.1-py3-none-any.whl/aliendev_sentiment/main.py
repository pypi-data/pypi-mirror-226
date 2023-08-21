import textwrap
from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    """
    A class for performing sentiment analysis on textual content.

    Attributes:
        content (str): The input content for sentiment analysis.
    """

    def __init__(self, content: str) -> None:
        """
        Initialize the SentimentAnalyzer object.

        Args:
            content (str): The input content for sentiment analysis.
        """
        self.content = content

    def _chunk_text(self, text):
        """
        Split the input text into chunks for translation.

        Args:
            text (str): The text to be chunked.

        Returns:
            list: A list of text chunks.
        """
        wrapper = textwrap.TextWrapper(width=4300)  # Adjusted width
        chunks = wrapper.wrap(text=text)
        
        for i, chunk in enumerate(chunks):
            if i < len(chunks) - 1:
                chunks[i] = f"{chunk} {chunks[i+1][:500]}"
        
        return chunks
    
    def _translate_to_english(self, text):
        """
        Translate the input text to English.

        Args:
            text (str): The text to be translated.

        Returns:
            str: Translated text in English.
        """
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    
    def _get_sentiment(self, text):
        """
        Perform sentiment analysis on the given text.

        Args:
            text (str): The text to be analyzed.

        Returns:
            str: Sentiment label ("Positive", "Neutral", "Negative").
        """
        analyzer = SentimentIntensityAnalyzer()
        sentiment_compound = analyzer.polarity_scores(text).get('compound')

        if sentiment_compound >= 0.05:
            return "Positive"
        elif sentiment_compound <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    
    def analyze_sentiment(self):
        """
        Analyze the sentiment of the content.

        Returns:
            str: Sentiment label ("Positive", "Neutral", "Negative").
        """
        chunks = self._chunk_text(self.content)
        translated_chunks = [self._translate_to_english(chunk) for chunk in chunks]
        
        combined_translation = ' '.join(translated_chunks)
        sentiment = self._get_sentiment(combined_translation)
        
        return sentiment

# Example usage
if __name__ == "__main__":
    input_content = "Your input text goes here."
    sentiment_analyzer = SentimentAnalyzer(input_content)
    result = sentiment_analyzer.analyze_sentiment()
    print("Sentiment:", result)
