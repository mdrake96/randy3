from PyPDF2 import PdfReader
from typing import Dict, List, Optional
import io
import re

class PDFProcessor:
    def __init__(self):
        """Initialize the PDF processor."""
        pass
    
    def process_pdf(self, file: bytes) -> Dict[str, any]:
        """
        Process a PDF file and extract its contents.
        
        Args:
            file (bytes): PDF file bytes
            
        Returns:
            Dict containing PDF information
        """
        try:
            # Create a PDF reader object
            pdf_reader = PdfReader(io.BytesIO(file))
            
            # Extract metadata
            metadata = pdf_reader.metadata
            
            # Extract text from all pages
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            # Clean text
            text = self._clean_text(text)
            
            # Extract basic information
            title = metadata.get('/Title', 'Untitled Document')
            author = metadata.get('/Author', 'Unknown Author')
            num_pages = len(pdf_reader.pages)
            
            return {
                'title': title,
                'author': author,
                'num_pages': num_pages,
                'text': text,
                'metadata': metadata
            }
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None
    
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