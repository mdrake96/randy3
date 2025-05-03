from typing import Dict, List, Any
import json
from datetime import datetime
from utils.web_scraper import WebScraper
from utils.feedback_system import FeedbackSystem, ReinforcementLearner
from utils.safety_system import SafetySystem

class AgentMemory:
    def __init__(self):
        self.memory_store = {}
        self.conversation_history = []
        self.search_history = []
        
    def store(self, key: str, value: Any):
        """Store information in memory"""
        self.memory_store[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        
    def retrieve(self, key: str) -> Any:
        """Retrieve information from memory"""
        return self.memory_store.get(key, {}).get('value')
    
    def add_to_history(self, role: str, content: str):
        """Add to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
    def add_to_search_history(self, query: str, results: List[Dict]):
        """Add to search history"""
        self.search_history.append({
            'query': query,
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
        
    def get_search_history(self) -> List[Dict]:
        """Get search history"""
        return self.search_history

class InputProcessor:
    def __init__(self, safety_system: SafetySystem):
        self.valid_input_types = ['research_topic', 'pdf_analysis', 'citation_request', 'web_search', 'feedback']
        self.safety_system = safety_system
        
    def process_input(self, input_data: Dict) -> Dict:
        """Process and validate user input"""
        # Validate input for safety
        is_valid, validation_message = self.safety_system.validate_input(input_data)
        if not is_valid:
            return {
                'type': 'error',
                'data': {
                    'message': validation_message,
                    'fallback_response': self.safety_system.get_fallback_response('input_validation')
                },
                'timestamp': datetime.now().isoformat(),
                'status': 'error'
            }
            
        input_type = input_data.get('type')
        if input_type not in self.valid_input_types:
            return {
                'type': 'error',
                'data': {
                    'message': f"Invalid input type. Must be one of {self.valid_input_types}",
                    'fallback_response': self.safety_system.get_fallback_response('unsupported')
                },
                'timestamp': datetime.now().isoformat(),
                'status': 'error'
            }
            
        processed_input = {
            'type': input_type,
            'data': input_data.get('data', {}),
            'timestamp': datetime.now().isoformat(),
            'status': 'processed'
        }
        
        return processed_input

class ReasoningEngine:
    def __init__(self, memory: AgentMemory, feedback_system: FeedbackSystem, reinforcement_learner: ReinforcementLearner, safety_system: SafetySystem):
        self.memory = memory
        self.web_scraper = WebScraper()
        self.feedback_system = feedback_system
        self.reinforcement_learner = reinforcement_learner
        self.safety_system = safety_system
        
    def analyze(self, processed_input: Dict) -> Dict:
        """Analyze input and determine appropriate actions"""
        if processed_input['status'] == 'error':
            return processed_input
            
        input_type = processed_input['type']
        
        # Enforce boundaries before processing
        if input_type in ['research_topic', 'web_search']:
            is_valid, boundary_message = self.safety_system.enforce_boundaries(
                input_type,
                processed_input['data']
            )
            if not is_valid:
                return {
                    'type': 'error',
                    'data': {
                        'message': boundary_message,
                        'fallback_response': self.safety_system.get_fallback_response('boundary_exceeded')
                    },
                    'timestamp': datetime.now().isoformat(),
                    'status': 'error'
                }
        
        try:
            if input_type == 'research_topic':
                return self._analyze_research_topic(processed_input)
            elif input_type == 'pdf_analysis':
                return self._analyze_pdf(processed_input)
            elif input_type == 'citation_request':
                return self._analyze_citation(processed_input)
            elif input_type == 'web_search':
                return self._analyze_web_search(processed_input)
            elif input_type == 'feedback':
                return self._process_feedback(processed_input)
        except Exception as e:
            return {
                'type': 'error',
                'data': {
                    'message': str(e),
                    'fallback_response': self.safety_system.get_fallback_response('error')
                },
                'timestamp': datetime.now().isoformat(),
                'status': 'error'
            }
            
    def _analyze_research_topic(self, input_data: Dict) -> Dict:
        """Analyze research topic request"""
        topic = input_data['data'].get('topic')
        
        # Get best parameters from reinforcement learner
        best_params = self.reinforcement_learner.get_best_actions('research')
        scope = best_params.get('scope', 'general')
        max_results = best_params.get('max_results', 5)
        
        return {
            'action': 'research',
            'parameters': {
                'topic': topic,
                'scope': scope,
                'max_results': max_results,
                'depth': 'comprehensive' if scope == 'detailed' else 'overview'
            }
        }
        
    def _analyze_pdf(self, input_data: Dict) -> Dict:
        """Analyze PDF analysis request"""
        # Get best parameters from reinforcement learner
        best_params = self.reinforcement_learner.get_best_actions('pdf_analysis')
        
        return {
            'action': 'process_pdf',
            'parameters': {
                'extract_metadata': best_params.get('extract_metadata', True),
                'detect_sections': best_params.get('detect_sections', True),
                'generate_summary': best_params.get('generate_summary', True)
            }
        }
        
    def _analyze_citation(self, input_data: Dict) -> Dict:
        """Analyze citation request"""
        return {
            'action': 'manage_citation',
            'parameters': {
                'format': input_data['data'].get('format', 'APA'),
                'style': input_data['data'].get('style', 'academic')
            }
        }
        
    def _analyze_web_search(self, input_data: Dict) -> Dict:
        """Analyze web search request"""
        query = input_data['data'].get('query')
        
        # Get best parameters from reinforcement learner
        best_params = self.reinforcement_learner.get_best_actions('web_search')
        max_results = best_params.get('max_results', 5)
        
        # Perform web search
        search_results = self.web_scraper.search(query, max_results=max_results)
        
        # Store in memory
        self.memory.add_to_search_history(query, search_results)
        
        return {
            'action': 'web_search',
            'parameters': {
                'query': query,
                'max_results': max_results
            },
            'results': search_results
        }
        
    def _process_feedback(self, input_data: Dict) -> Dict:
        """Process user feedback"""
        feedback_data = input_data['data']
        action_type = feedback_data.get('action_type')
        reward = feedback_data.get('reward', 0.0)
        action_params = feedback_data.get('action_params', {})
        
        # Record feedback
        self.feedback_system.record_feedback(action_type, feedback_data)
        
        # Update action values
        self.reinforcement_learner.update_action_values(action_type, action_params, reward)
        
        # Adjust learning rates
        self.feedback_system.adjust_learning_rates()
        
        return {
            'action': 'process_feedback',
            'parameters': {
                'action_type': action_type,
                'reward': reward
            }
        }

class OutputGenerator:
    def __init__(self, memory: AgentMemory, feedback_system: FeedbackSystem, safety_system: SafetySystem):
        self.memory = memory
        self.feedback_system = feedback_system
        self.safety_system = safety_system
        
    def generate_response(self, analysis_result: Dict, raw_data: Any = None) -> Dict:
        """Generate structured response based on analysis"""
        if analysis_result['status'] == 'error':
            return analysis_result
            
        response = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'action': analysis_result['action'],
            'data': raw_data if raw_data else {},
            'metadata': {
                'processing_time': datetime.now().isoformat(),
                'source': 'agent_system',
                'performance_metrics': self.feedback_system.get_performance_metrics(),
                'safety_metrics': self.safety_system.get_safety_metrics(),
                'boundaries': self.safety_system.get_boundaries()
            }
        }
        
        # Include search results if available
        if analysis_result.get('results'):
            response['data']['search_results'] = analysis_result['results']
        
        # Store the response in memory
        self.memory.store(f"response_{datetime.now().timestamp()}", response)
        
        return response
        
    def format_for_display(self, response: Dict) -> Dict:
        """Format response for display in the UI"""
        if response['status'] == 'error':
            return {
                'title': "Error",
                'content': response['data']['fallback_response'],
                'metadata': {
                    'error_message': response['data']['message']
                },
                'timestamp': response['timestamp']
            }
            
        display_format = {
            'title': f"Agent Response - {response['action']}",
            'content': response['data'],
            'metadata': response['metadata'],
            'timestamp': response['timestamp']
        }
        
        return display_format

class AgentSystem:
    def __init__(self):
        self.memory = AgentMemory()
        self.feedback_system = FeedbackSystem()
        self.safety_system = SafetySystem()
        self.reinforcement_learner = ReinforcementLearner(self.feedback_system)
        self.input_processor = InputProcessor(self.safety_system)
        self.reasoning_engine = ReasoningEngine(
            self.memory,
            self.feedback_system,
            self.reinforcement_learner,
            self.safety_system
        )
        self.output_generator = OutputGenerator(
            self.memory,
            self.feedback_system,
            self.safety_system
        )
        
    def process(self, input_data: Dict) -> Dict:
        """Process input through the complete agent system"""
        # 1. Process input
        processed_input = self.input_processor.process_input(input_data)
        
        # 2. Store in memory
        self.memory.store('last_input', processed_input)
        
        # 3. Reason about the input
        analysis_result = self.reasoning_engine.analyze(processed_input)
        
        # 4. Generate output
        response = self.output_generator.generate_response(analysis_result)
        
        # 5. Add to conversation history
        self.memory.add_to_history('user', str(input_data))
        self.memory.add_to_history('agent', str(response))
        
        return response 