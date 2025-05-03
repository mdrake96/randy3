from typing import Dict, List, Any
import json
from datetime import datetime
import numpy as np

class FeedbackSystem:
    def __init__(self):
        self.feedback_history = []
        self.performance_metrics = {
            'research_accuracy': 0.0,
            'pdf_analysis_quality': 0.0,
            'search_relevance': 0.0,
            'response_time': 0.0
        }
        self.learning_rates = {
            'research': 0.1,
            'pdf_analysis': 0.1,
            'web_search': 0.1
        }
        
    def record_feedback(self, action_type: str, feedback_data: Dict):
        """Record user feedback for a specific action"""
        feedback_entry = {
            'action_type': action_type,
            'feedback_data': feedback_data,
            'timestamp': datetime.now().isoformat()
        }
        self.feedback_history.append(feedback_entry)
        self._update_performance_metrics(feedback_entry)
        
    def _update_performance_metrics(self, feedback_entry: Dict):
        """Update performance metrics based on feedback"""
        action_type = feedback_entry['action_type']
        feedback = feedback_entry['feedback_data']
        
        if action_type == 'research':
            self.performance_metrics['research_accuracy'] = (
                0.9 * self.performance_metrics['research_accuracy'] +
                0.1 * feedback.get('accuracy', 0.0)
            )
        elif action_type == 'pdf_analysis':
            self.performance_metrics['pdf_analysis_quality'] = (
                0.9 * self.performance_metrics['pdf_analysis_quality'] +
                0.1 * feedback.get('quality', 0.0)
            )
        elif action_type == 'web_search':
            self.performance_metrics['search_relevance'] = (
                0.9 * self.performance_metrics['search_relevance'] +
                0.1 * feedback.get('relevance', 0.0)
            )
            
        # Update response time metric
        self.performance_metrics['response_time'] = (
            0.9 * self.performance_metrics['response_time'] +
            0.1 * feedback.get('response_time', 0.0)
        )
        
    def get_performance_metrics(self) -> Dict:
        """Get current performance metrics"""
        return self.performance_metrics
        
    def adjust_learning_rates(self):
        """Adjust learning rates based on performance metrics"""
        for action_type in self.learning_rates:
            if action_type == 'research':
                metric = self.performance_metrics['research_accuracy']
            elif action_type == 'pdf_analysis':
                metric = self.performance_metrics['pdf_analysis_quality']
            else:
                metric = self.performance_metrics['search_relevance']
                
            # Adjust learning rate based on performance
            if metric < 0.5:
                self.learning_rates[action_type] = min(0.2, self.learning_rates[action_type] * 1.1)
            else:
                self.learning_rates[action_type] = max(0.05, self.learning_rates[action_type] * 0.95)
                
    def get_feedback_history(self) -> List[Dict]:
        """Get feedback history"""
        return self.feedback_history
        
    def get_learning_rates(self) -> Dict:
        """Get current learning rates"""
        return self.learning_rates

class ReinforcementLearner:
    def __init__(self, feedback_system: FeedbackSystem):
        self.feedback_system = feedback_system
        self.action_values = {
            'research': {
                'scope': {'general': 0.5, 'detailed': 0.5},
                'max_results': {5: 0.5, 10: 0.5}
            },
            'pdf_analysis': {
                'extract_metadata': True,
                'detect_sections': True,
                'generate_summary': True
            },
            'web_search': {
                'max_results': {5: 0.5, 10: 0.5}
            }
        }
        
    def update_action_values(self, action_type: str, action_params: Dict, reward: float):
        """Update action values based on received reward"""
        if action_type not in self.action_values:
            return
            
        learning_rate = self.feedback_system.learning_rates[action_type]
        
        for param, value in action_params.items():
            if param in self.action_values[action_type]:
                if isinstance(self.action_values[action_type][param], dict):
                    if value in self.action_values[action_type][param]:
                        current_value = self.action_values[action_type][param][value]
                        new_value = current_value + learning_rate * (reward - current_value)
                        self.action_values[action_type][param][value] = new_value
                else:
                    # For boolean parameters, update based on reward
                    if reward > 0.5:
                        self.action_values[action_type][param] = True
                    else:
                        self.action_values[action_type][param] = False
                        
    def get_best_actions(self, action_type: str) -> Dict:
        """Get the best action parameters based on learned values"""
        if action_type not in self.action_values:
            return {}
            
        best_actions = {}
        for param, values in self.action_values[action_type].items():
            if isinstance(values, dict):
                best_value = max(values.items(), key=lambda x: x[1])[0]
                best_actions[param] = best_value
            else:
                best_actions[param] = values
                
        return best_actions 