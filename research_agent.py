import os
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import openai
from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm

class ResearchAgent:
    def __init__(self):
        """Initialize the research agent with necessary configurations."""
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        openai.api_key = self.api_key
        
        self.sources = []
        self.citations = []
        
    def research_topic(self, topic: str, max_sources: int = 5, include_citations: bool = True) -> Dict[str, Any]:
        """
        Research a given topic and gather information from multiple sources.
        
        Args:
            topic (str): The research topic
            max_sources (int): Maximum number of sources to gather
            include_citations (bool): Whether to include citations
            
        Returns:
            Dict containing research results
        """
        # Search for relevant sources
        search_results = self._search_sources(topic, max_sources)
        
        # Process and evaluate each source
        processed_sources = []
        for source in tqdm(search_results, desc="Processing sources"):
            content = self._extract_content(source['url'])
            if content:
                summary = self._summarize_content(content)
                credibility = self._evaluate_credibility(source['url'], content)
                
                processed_sources.append({
                    'url': source['url'],
                    'title': source['title'],
                    'summary': summary,
                    'credibility_score': credibility,
                    'content': content
                })
                
                if include_citations:
                    citation = self._generate_citation(source)
                    self.citations.append(citation)
        
        self.sources = processed_sources
        return {
            'topic': topic,
            'sources': processed_sources,
            'citations': self.citations if include_citations else None
        }
    
    def generate_report(self, research_results: Dict[str, Any]) -> str:
        """
        Generate a structured report from research results.
        
        Args:
            research_results (Dict): Results from research_topic
            
        Returns:
            str: Formatted report
        """
        report = f"# Research Report: {research_results['topic']}\n\n"
        report += "## Summary\n\n"
        
        # Generate overall summary
        summaries = [source['summary'] for source in research_results['sources']]
        overall_summary = self._generate_overall_summary(summaries)
        report += f"{overall_summary}\n\n"
        
        # Add detailed source information
        report += "## Sources\n\n"
        for source in research_results['sources']:
            report += f"### {source['title']}\n"
            report += f"**URL:** {source['url']}\n"
            report += f"**Credibility Score:** {source['credibility_score']}/10\n"
            report += f"**Summary:** {source['summary']}\n\n"
        
        # Add citations if available
        if research_results['citations']:
            report += "## References\n\n"
            for citation in research_results['citations']:
                report += f"- {citation}\n"
        
        return report
    
    def _search_sources(self, topic: str, max_sources: int) -> List[Dict[str, str]]:
        """Search for relevant sources using web search APIs."""
        # This is a placeholder - in a real implementation, you would use
        # a search API like Google Custom Search or Bing Search
        # For now, we'll return some example sources
        return [
            {
                'url': 'https://example.com/source1',
                'title': 'Example Source 1'
            },
            {
                'url': 'https://example.com/source2',
                'title': 'Example Source 2'
            }
        ]
    
    def _extract_content(self, url: str) -> str:
        """Extract content from a webpage."""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text()
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return ""
    
    def _summarize_content(self, content: str) -> str:
        """Summarize content using OpenAI's API."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant. Summarize the following content concisely."},
                    {"role": "user", "content": content[:4000]}  # Limit content length
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error summarizing content: {str(e)}")
            return ""
    
    def _evaluate_credibility(self, url: str, content: str) -> float:
        """Evaluate the credibility of a source."""
        # This is a simplified implementation
        # In a real application, you would use more sophisticated methods
        credibility_factors = {
            'domain_authority': self._check_domain_authority(url),
            'content_quality': self._evaluate_content_quality(content),
            'recency': self._check_recency(url)
        }
        return sum(credibility_factors.values()) / len(credibility_factors)
    
    def _generate_citation(self, source: Dict[str, str]) -> str:
        """Generate a citation for a source."""
        # This is a simplified implementation
        # In a real application, you would use a proper citation style
        return f"{source['title']}. Retrieved from {source['url']} on {datetime.now().strftime('%Y-%m-%d')}"
    
    def _generate_overall_summary(self, summaries: List[str]) -> str:
        """Generate an overall summary from multiple source summaries."""
        combined_summaries = "\n\n".join(summaries)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant. Create a coherent overall summary from these individual summaries."},
                    {"role": "user", "content": combined_summaries}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating overall summary: {str(e)}")
            return "Error generating overall summary"
    
    def _check_domain_authority(self, url: str) -> float:
        """Check the authority of a domain."""
        # Simplified implementation
        # In a real application, you would use domain authority metrics
        return 0.7
    
    def _evaluate_content_quality(self, content: str) -> float:
        """Evaluate the quality of content."""
        # Simplified implementation
        # In a real application, you would use more sophisticated methods
        return 0.8
    
    def _check_recency(self, url: str) -> float:
        """Check how recent the content is."""
        # Simplified implementation
        # In a real application, you would check the last modified date
        return 0.9 