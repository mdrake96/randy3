import openai
from typing import List, Dict, Any
import re
from datetime import datetime

class ContentSummarizer:
    def __init__(self, api_key: str):
        """Initialize the summarizer with OpenAI API key."""
        self.api_key = api_key
        openai.api_key = api_key
    
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """
        Summarize a given text using OpenAI's API.
        
        Args:
            text (str): The text to summarize
            max_length (int): Maximum length of the summary
            
        Returns:
            str: The summarized text
        """
        try:
            # Truncate text if it's too long
            if len(text) > 4000:
                text = text[:4000] + "..."
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful research assistant. Summarize the following text in {max_length} words or less, focusing on key points and main ideas."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error summarizing text: {str(e)}")
            return "Error generating summary"
    
    def generate_key_points(self, text: str, num_points: int = 5) -> List[str]:
        """
        Generate key points from a text.
        
        Args:
            text (str): The text to analyze
            num_points (int): Number of key points to generate
            
        Returns:
            List[str]: List of key points
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful research assistant. Extract {num_points} key points from the following text. Format each point as a concise bullet point."},
                    {"role": "user", "content": text}
                ]
            )
            points = response.choices[0].message.content
            return [point.strip() for point in points.split('\n') if point.strip()]
        except Exception as e:
            print(f"Error generating key points: {str(e)}")
            return []
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment and tone of a text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            Dict containing sentiment analysis results
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant. Analyze the sentiment and tone of the following text. Provide a brief analysis of the overall sentiment (positive, negative, neutral) and the tone (formal, informal, academic, etc.)."},
                    {"role": "user", "content": text}
                ]
            )
            analysis = response.choices[0].message.content
            return {
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return {
                'analysis': 'Error analyzing sentiment',
                'timestamp': datetime.now().isoformat()
            }
    
    def extract_quotes(self, text: str, max_quotes: int = 3) -> List[str]:
        """
        Extract notable quotes from a text.
        
        Args:
            text (str): The text to analyze
            max_quotes (int): Maximum number of quotes to extract
            
        Returns:
            List[str]: List of notable quotes
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful research assistant. Extract {max_quotes} notable quotes from the following text. Each quote should be significant and meaningful."},
                    {"role": "user", "content": text}
                ]
            )
            quotes = response.choices[0].message.content
            return [quote.strip() for quote in quotes.split('\n') if quote.strip()]
        except Exception as e:
            print(f"Error extracting quotes: {str(e)}")
            return [] 