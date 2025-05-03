from typing import Dict, List, Any, Tuple
import re
from datetime import datetime

class SafetySystem:
    def __init__(self):
        # Define safety boundaries
        self.boundaries = {
            'max_file_size_mb': 10,  # Maximum PDF file size
            'max_search_results': 10,  # Maximum number of search results
            'max_research_sources': 10,  # Maximum number of research sources
            'max_response_length': 5000,  # Maximum response length in characters
            'timeout_seconds': 30,  # Maximum processing time
        }
        
        # Define restricted patterns
        self.restricted_patterns = {
            'inappropriate_content': [
                r'porn|explicit|nsfw',
                r'hate speech|racism|discrimination',
                r'violence|harm|dangerous',
                r'personal information|privacy violation',
                r'malware|virus|exploit'
            ],
            'sensitive_topics': [
                r'classified|confidential|secret',
                r'medical records|health information',
                r'financial data|banking information',
                r'government secrets|national security'
            ]
        }
        
        # Define fallback responses
        self.fallback_responses = {
            'input_validation': "I'm sorry, but I can't process that request due to content restrictions.",
            'boundary_exceeded': "I'm sorry, but that request exceeds my operational boundaries.",
            'timeout': "I'm sorry, but the request took too long to process.",
            'error': "I'm sorry, but I encountered an error while processing your request.",
            'unsupported': "I'm sorry, but I can't perform that specific action."
        }
        
        # Initialize safety metrics
        self.safety_metrics = {
            'blocked_requests': 0,
            'warnings_issued': 0,
            'fallbacks_used': 0,
            'last_incident': None
        }
        
    def validate_input(self, input_data: Dict) -> Tuple[bool, str]:
        """Validate input for safety and appropriateness"""
        # Check for empty input
        if not input_data:
            return False, "Empty input provided"
            
        # Check input type
        if 'type' not in input_data:
            return False, "Missing input type"
            
        # Check input data
        if 'data' not in input_data:
            return False, "Missing input data"
            
        # Validate content based on input type
        if input_data['type'] == 'research_topic':
            return self._validate_research_topic(input_data['data'])
        elif input_data['type'] == 'pdf_analysis':
            return self._validate_pdf_analysis(input_data['data'])
        elif input_data['type'] == 'web_search':
            return self._validate_web_search(input_data['data'])
        elif input_data['type'] == 'feedback':
            return self._validate_feedback(input_data['data'])
            
        return True, "Input validated successfully"
        
    def _validate_research_topic(self, data: Dict) -> Tuple[bool, str]:
        """Validate research topic input"""
        if 'topic' not in data:
            return False, "Missing research topic"
            
        # Check for restricted content
        topic = data['topic'].lower()
        for pattern in self.restricted_patterns['inappropriate_content']:
            if re.search(pattern, topic):
                self.safety_metrics['blocked_requests'] += 1
                self.safety_metrics['last_incident'] = datetime.now().isoformat()
                return False, "Research topic contains restricted content"
                
        # Check for sensitive topics
        for pattern in self.restricted_patterns['sensitive_topics']:
            if re.search(pattern, topic):
                self.safety_metrics['warnings_issued'] += 1
                return False, "Research topic involves sensitive information"
                
        return True, "Research topic validated successfully"
        
    def _validate_pdf_analysis(self, data: Dict) -> Tuple[bool, str]:
        """Validate PDF analysis input"""
        if 'file_size' not in data:
            return False, "Missing file size information"
            
        # Check file size boundary
        if data['file_size'] > self.boundaries['max_file_size_mb'] * 1024 * 1024:
            self.safety_metrics['boundary_exceeded'] += 1
            return False, f"File size exceeds maximum limit of {self.boundaries['max_file_size_mb']}MB"
            
        return True, "PDF analysis request validated successfully"
        
    def _validate_web_search(self, data: Dict) -> Tuple[bool, str]:
        """Validate web search input"""
        if 'query' not in data:
            return False, "Missing search query"
            
        # Check for restricted content
        query = data['query'].lower()
        for pattern in self.restricted_patterns['inappropriate_content']:
            if re.search(pattern, query):
                self.safety_metrics['blocked_requests'] += 1
                self.safety_metrics['last_incident'] = datetime.now().isoformat()
                return False, "Search query contains restricted content"
                
        # Check for sensitive topics
        for pattern in self.restricted_patterns['sensitive_topics']:
            if re.search(pattern, query):
                self.safety_metrics['warnings_issued'] += 1
                return False, "Search query involves sensitive information"
                
        return True, "Web search request validated successfully"
        
    def _validate_feedback(self, data: Dict) -> Tuple[bool, str]:
        """Validate feedback input"""
        if 'action_type' not in data:
            return False, "Missing action type in feedback"
            
        if 'reward' not in data:
            return False, "Missing reward value in feedback"
            
        # Validate reward value
        if not 0 <= data['reward'] <= 1:
            return False, "Invalid reward value (must be between 0 and 1)"
            
        return True, "Feedback validated successfully"
        
    def enforce_boundaries(self, action_type: str, parameters: Dict) -> Tuple[bool, str]:
        """Enforce operational boundaries"""
        if action_type == 'research':
            if parameters.get('max_results', 0) > self.boundaries['max_research_sources']:
                return False, f"Maximum research sources exceeded (limit: {self.boundaries['max_research_sources']})"
                
        elif action_type == 'web_search':
            if parameters.get('max_results', 0) > self.boundaries['max_search_results']:
                return False, f"Maximum search results exceeded (limit: {self.boundaries['max_search_results']})"
                
        return True, "Boundaries enforced successfully"
        
    def get_fallback_response(self, fallback_type: str) -> str:
        """Get appropriate fallback response"""
        self.safety_metrics['fallbacks_used'] += 1
        return self.fallback_responses.get(fallback_type, self.fallback_responses['error'])
        
    def get_safety_metrics(self) -> Dict:
        """Get current safety metrics"""
        return self.safety_metrics
        
    def get_boundaries(self) -> Dict:
        """Get current operational boundaries"""
        return self.boundaries
        
    def get_restricted_patterns(self) -> Dict:
        """Get restricted content patterns"""
        return self.restricted_patterns 