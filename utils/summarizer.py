"""
Text summarization utilities.
"""

from openai import OpenAI
from typing import List, Dict, Any, Optional
import re
from datetime import datetime

def summarize_text(text: str, api_key: str, max_length: int = 1000) -> str:
    """
    Summarize text using OpenAI's API.
    
    Args:
        text (str): Text to summarize
        api_key (str): OpenAI API key
        max_length (int): Maximum length of the summary
        
    Returns:
        str: Generated summary
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Truncate text if it's too long
        if len(text) > 4000:
            text = text[:4000] + "..."
        
        # Generate summary
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful research assistant that creates concise summaries."},
                {"role": "user", "content": f"Please summarize the following text in {max_length} characters or less:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return "Error generating summary. Please try again."

def generate_key_points(text: str, api_key: str = None, num_points: int = 5) -> List[str]:
    """
    Generate key points from a text.
    
    Args:
        text (str): The text to analyze
        api_key (str): OpenAI API key
        num_points (int): Number of key points to generate
        
    Returns:
        List[str]: List of key points
    """
    client = OpenAI(api_key=api_key)
        
    try:
        response = client.chat.completions.create(
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

def analyze_sentiment(text: str, api_key: str = None) -> Dict[str, Any]:
    """
    Analyze the sentiment and tone of a text.
    
    Args:
        text (str): The text to analyze
        api_key (str): OpenAI API key
        
    Returns:
        Dict containing sentiment analysis results
    """
    client = OpenAI(api_key=api_key)
        
    try:
        response = client.chat.completions.create(
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

def extract_quotes(text: str, api_key: str = None, max_quotes: int = 3) -> List[str]:
    """
    Extract notable quotes from a text.
    
    Args:
        text (str): The text to analyze
        api_key (str): OpenAI API key
        max_quotes (int): Maximum number of quotes to extract
        
    Returns:
        List[str]: List of notable quotes
    """
    client = OpenAI(api_key=api_key)
        
    try:
        response = client.chat.completions.create(
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