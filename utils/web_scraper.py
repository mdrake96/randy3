import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import re
from urllib.parse import urlparse

class WebScraper:
    def __init__(self):
        """Initialize the web scraper with default settings."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape an article from a given URL.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            Optional[Dict] containing article information
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract main content
            content = self._extract_content(soup)
            
            # Extract metadata
            metadata = self._extract_metadata(soup)
            
            return {
                'title': title,
                'content': content,
                'url': url,
                'metadata': metadata
            }
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the title of the article."""
        title = soup.find('title')
        if title:
            return title.text.strip()
        
        # Try alternative title tags
        for tag in ['h1', 'h2']:
            title = soup.find(tag)
            if title:
                return title.text.strip()
        
        return "Untitled"
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract the main content of the article."""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Common content containers
        content_containers = [
            'article',
            'main',
            '.article-content',
            '.post-content',
            '#content',
            '.content'
        ]
        
        for selector in content_containers:
            content = soup.select_one(selector)
            if content:
                return self._clean_text(content.get_text())
        
        # Fallback: get all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            return self._clean_text('\n'.join(p.get_text() for p in paragraphs))
        
        return ""
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract metadata from the page."""
        metadata = {}
        
        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', meta.get('property', ''))
            content = meta.get('content', '')
            if name and content:
                metadata[name] = content
        
        # Extract publication date
        date = self._extract_date(soup)
        if date:
            metadata['publication_date'] = date
        
        return metadata
    
    def _extract_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract the publication date from the page."""
        # Common date selectors
        date_selectors = [
            'time',
            '.date',
            '.published',
            '.post-date',
            '[datetime]'
        ]
        
        for selector in date_selectors:
            date_element = soup.select_one(selector)
            if date_element:
                date = date_element.get('datetime') or date_element.text
                if date:
                    return date.strip()
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text 