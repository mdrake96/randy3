from typing import Dict, List, Optional
from datetime import datetime
import re

class CitationManager:
    def __init__(self):
        """Initialize the citation manager."""
        self.citation_styles = {
            'apa': self._format_apa,
            'mla': self._format_mla,
            'chicago': self._format_chicago
        }
    
    def generate_citation(self, source: Dict[str, str], style: str = 'apa') -> str:
        """
        Generate a citation for a source in the specified style.
        
        Args:
            source (Dict): Source information
            style (str): Citation style (apa, mla, chicago)
            
        Returns:
            str: Formatted citation
        """
        if style not in self.citation_styles:
            raise ValueError(f"Unsupported citation style: {style}")
        
        return self.citation_styles[style](source)
    
    def _format_apa(self, source: Dict[str, str]) -> str:
        """Format citation in APA style."""
        author = source.get('author', 'Unknown')
        title = source.get('title', 'Untitled')
        url = source.get('url', '')
        date = source.get('date', datetime.now().strftime('%Y, %B %d'))
        
        return f"{author}. ({date}). {title}. Retrieved from {url}"
    
    def _format_mla(self, source: Dict[str, str]) -> str:
        """Format citation in MLA style."""
        author = source.get('author', 'Unknown')
        title = source.get('title', 'Untitled')
        url = source.get('url', '')
        date = source.get('date', datetime.now().strftime('%d %B %Y'))
        
        return f"{author}. \"{title}.\" {date}, {url}"
    
    def _format_chicago(self, source: Dict[str, str]) -> str:
        """Format citation in Chicago style."""
        author = source.get('author', 'Unknown')
        title = source.get('title', 'Untitled')
        url = source.get('url', '')
        date = source.get('date', datetime.now().strftime('%B %d, %Y'))
        
        return f"{author}. \"{title}.\" Accessed {date}. {url}"
    
    def extract_metadata(self, text: str) -> Dict[str, str]:
        """
        Extract metadata from a text that could be used for citations.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict containing extracted metadata
        """
        metadata = {}
        
        # Extract potential author names
        author_patterns = [
            r'by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'Author:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'Written by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)'
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, text)
            if match:
                metadata['author'] = match.group(1)
                break
        
        # Extract potential dates
        date_patterns = [
            r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})',
            r'([A-Za-z]+\s+\d{1,2},\s+\d{4})',
            r'(\d{4}-\d{2}-\d{2})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                metadata['date'] = match.group(1)
                break
        
        return metadata
    
    def validate_citation(self, citation: str, style: str) -> bool:
        """
        Validate if a citation follows the specified style guidelines.
        
        Args:
            citation (str): The citation to validate
            style (str): Citation style
            
        Returns:
            bool: True if citation is valid
        """
        # Basic validation patterns for each style
        validation_patterns = {
            'apa': r'.*\(\d{4}\).*Retrieved from.*',
            'mla': r'.*\"[^\"]+\".*\d{1,2}\s+[A-Za-z]+\s+\d{4}.*',
            'chicago': r'.*\"[^\"]+\".*Accessed.*'
        }
        
        if style not in validation_patterns:
            return False
        
        return bool(re.match(validation_patterns[style], citation))
    
    def generate_bibliography(self, sources: List[Dict[str, str]], style: str = 'apa') -> str:
        """
        Generate a bibliography from multiple sources.
        
        Args:
            sources (List[Dict]): List of source information
            style (str): Citation style
            
        Returns:
            str: Formatted bibliography
        """
        citations = [self.generate_citation(source, style) for source in sources]
        return "\n\n".join(citations) 