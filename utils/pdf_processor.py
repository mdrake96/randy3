"""
PDF processing utilities for research assistant.
"""

from PyPDF2 import PdfReader
from typing import Dict, List, Any
import io
import re

class PDFProcessor:
    def __init__(self):
        """Initialize the PDF processor."""
        pass
    
    def process_pdf(self, file) -> Dict[str, Any]:
        """
        Process a PDF file and extract its content.
        
        Args:
            file: File object or bytes of the PDF
            
        Returns:
            Dict containing metadata, sections, and full text
        """
        try:
            # Read PDF file
            pdf_reader = PdfReader(file)
            
            # Extract metadata
            metadata = {
                'title': pdf_reader.metadata.title or 'Untitled',
                'author': pdf_reader.metadata.author or 'Unknown',
                'page_count': len(pdf_reader.pages)
            }
            
            # Extract text from all pages
            full_text = ""
            sections = []
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                full_text += page_text + "\n"
                
                # Create a section for each page
                sections.append({
                    'title': f"Page {page_num}",
                    'content': page_text
                })
            
            return {
                'metadata': metadata,
                'sections': sections,
                'full_text': full_text.strip()
            }
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return {
                'metadata': {
                    'title': 'Error',
                    'author': 'Error',
                    'page_count': 0
                },
                'sections': [],
                'full_text': ''
            }
    
    def extract_sections(self, text: str) -> List[Dict[str, str]]:
        """
        Extract sections from PDF text.
        
        Args:
            text (str): PDF text content
            
        Returns:
            List of sections with titles and content
        """
        # Common section patterns
        section_patterns = [
            r'\n([A-Z][A-Za-z\s]+)\n',  # All caps titles
            r'\n(\d+\.\s+[A-Za-z\s]+)\n',  # Numbered sections
            r'\n([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\n'  # Title case sections
        ]
        
        sections = []
        current_section = {'title': 'Introduction', 'content': ''}
        
        # Split text into lines
        lines = text.split('\n')
        
        for line in lines:
            # Check if line matches any section pattern
            is_section = False
            for pattern in section_patterns:
                if re.match(pattern, '\n' + line + '\n'):
                    # Save previous section
                    if current_section['content']:
                        sections.append(current_section)
                    # Start new section
                    current_section = {'title': line.strip(), 'content': ''}
                    is_section = True
                    break
            
            if not is_section:
                current_section['content'] += line + '\n'
        
        # Add the last section
        if current_section['content']:
            sections.append(current_section)
        
        return sections
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text from PDF.
        
        Args:
            text (str): Raw text from PDF
            
        Returns:
            str: Cleaned text
        """
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove page numbers and headers/footers
        text = re.sub(r'\n\d+\n', '\n', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters
        text = re.sub(r'[^\w\s.,;:!?()\-\n]', '', text)
        
        return text.strip()