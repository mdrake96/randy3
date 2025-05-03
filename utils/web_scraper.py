"""
Web scraping utilities for research assistant.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import re
from datetime import datetime
import time
import random

class WebScraper:
    def __init__(self):
        """Initialize the web scraper with necessary configurations."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search(self, query: str, max_results: int = 5, search_type: str = "general") -> List[Dict]:
        """
        Perform a web search and return results.
        This is a placeholder implementation that returns example results.
        In a real application, you would integrate with a search API like Google Custom Search.
        """
        # Example results for demonstration
        example_results = [
            {
                'title': 'Example Research Paper 1',
                'url': 'https://example.com/paper1',
                'snippet': 'This is an example research paper about the topic you searched for.'
            },
            {
                'title': 'Example Research Paper 2',
                'url': 'https://example.com/paper2',
                'snippet': 'Another example research paper with relevant information.'
            },
            {
                'title': 'Example News Article',
                'url': 'https://example.com/news1',
                'snippet': 'A news article related to your search query.'
            }
        ]
        return example_results[:max_results]
    
    def scrape_article(self, url: str) -> Optional[str]:
        """
        Scrape the main content from a web article.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error scraping article: {str(e)}")
            return None
    
    def extract_metadata(self, url: str) -> Dict[str, str]:
        """
        Extract metadata from a webpage.
        
        Args:
            url (str): URL of the webpage
            
        Returns:
            Dict[str, str]: Extracted metadata
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            metadata = {
                'title': soup.title.string if soup.title else '',
                'description': '',
                'author': '',
                'date': ''
            }
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                metadata['description'] = meta_desc.get('content', '')
            
            # Extract author
            meta_author = soup.find('meta', attrs={'name': 'author'})
            if meta_author:
                metadata['author'] = meta_author.get('content', '')
            
            # Extract date
            meta_date = soup.find('meta', attrs={'property': 'article:published_time'})
            if meta_date:
                metadata['date'] = meta_date.get('content', '')
            
            return metadata
        except Exception as e:
            print(f"Error extracting metadata from {url}: {str(e)}")
            return {
                'title': '',
                'description': '',
                'author': '',
                'date': ''
            } 