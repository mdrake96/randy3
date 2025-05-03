"""
Utility modules for research assistant.
"""

from .web_scraper import WebScraper
from .summarizer import summarize_text
from .pdf_processor import PDFProcessor

__all__ = ['WebScraper', 'summarize_text', 'PDFProcessor'] 