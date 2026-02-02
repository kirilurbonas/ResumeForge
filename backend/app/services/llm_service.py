"""LLM service for generating resume improvement suggestions."""

from typing import List, Optional, AsyncIterator
import os
from abc import ABC, abstractmethod


class LLMService(ABC):
    """Abstract base class for LLM services."""
    
    @abstractmethod
    async def generate_suggestions(
        self,
        resume_text: str,
        analysis_results: dict,
        suggestion_type: str = "general"
    ) -> str:
        """Generate improvement suggestions for resume."""
        pass
    
    @abstractmethod
    async def stream_suggestions(
        self,
        resume_text: str,
        analysis_results: dict,
        suggestion_type: str = "general"
    ) -> AsyncIterator[str]:
        """Stream suggestions."""
        pass


class OpenAIService(LLMService):
    """OpenAI LLM service implementation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI service.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model name to use
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package is required. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def _build_suggestion_prompt(self, resume_text: str, analysis_results: dict, suggestion_type: str) -> str:
        """Build prompt for resume suggestions."""
        ats_score = analysis_results.get('ats_score', 0)
        strengths = analysis_results.get('strengths', [])
        weaknesses = analysis_results.get('weaknesses', [])
        
        prompt = f"""You are an expert resume writer and career coach. Analyze this resume and provide specific, actionable improvement suggestions.

Resume Text:
{resume_text[:2000]}  # Limit to first 2000 chars

Current Analysis:
- ATS Score: {ats_score}/100
- Strengths: {', '.join(strengths[:5]) if strengths else 'None'}
- Weaknesses: {', '.join(weaknesses[:5]) if weaknesses else 'None'}

Please provide {suggestion_type} improvement suggestions. Be specific and actionable. Format your response as a bulleted list of suggestions.

Suggestions:"""
        
        return prompt
    
    async def generate_suggestions(
        self,
        resume_text: str,
        analysis_results: dict,
        suggestion_type: str = "general"
    ) -> str:
        """Generate improvement suggestions using OpenAI API."""
        prompt = self._build_suggestion_prompt(resume_text, analysis_results, suggestion_type)
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert resume writer and career coach. Provide specific, actionable suggestions to improve resumes."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating suggestions: {str(e)}"
    
    async def stream_suggestions(
        self,
        resume_text: str,
        analysis_results: dict,
        suggestion_type: str = "general"
    ) -> AsyncIterator[str]:
        """Stream suggestions using OpenAI API."""
        prompt = self._build_suggestion_prompt(resume_text, analysis_results, suggestion_type)
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert resume writer and career coach. Provide specific, actionable suggestions to improve resumes."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error generating suggestions: {str(e)}"
    
    async def generate_action_verbs(self, job_description: str = None) -> List[str]:
        """Generate strong action verb suggestions."""
        prompt = """Provide a list of 10-15 strong action verbs that are effective for resume bullet points. 
Focus on verbs that demonstrate impact and achievement (e.g., 'achieved', 'implemented', 'optimized').
Format as a simple comma-separated list."""
        
        messages = [
            {"role": "system", "content": "You are a resume writing expert."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )
            
            content = response.choices[0].message.content
            # Parse comma-separated list
            verbs = [v.strip() for v in content.split(',')]
            return verbs[:15]
        except Exception as e:
            # Fallback to default verbs
            return [
                'achieved', 'improved', 'increased', 'developed', 'created',
                'designed', 'implemented', 'managed', 'led', 'optimized',
                'enhanced', 'streamlined', 'established', 'launched', 'built'
            ]
    
    async def rewrite_section(self, section_text: str, section_type: str = "experience") -> str:
        """Rewrite a resume section to be more impactful."""
        prompt = f"""Rewrite this {section_type} section from a resume to be more impactful and use stronger action verbs. 
Keep it concise and focused on achievements.

Original:
{section_text}

Rewritten:"""
        
        messages = [
            {"role": "system", "content": "You are an expert resume writer. Rewrite sections to be more impactful."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return section_text  # Return original on error


def get_llm_service(provider: str = "openai", **kwargs) -> LLMService:
    """
    Factory function to get LLM service instance.
    
    Args:
        provider: LLM provider ("openai" or "local")
        **kwargs: Additional arguments for the service
        
    Returns:
        LLMService instance
    """
    provider = provider.lower()
    
    if provider == "openai":
        return OpenAIService(**kwargs)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Only 'openai' is supported.")


# Default instance (will be initialized in routes)
llm_service = None

def initialize_llm_service():
    """Initialize the global LLM service instance."""
    global llm_service
    provider = os.getenv("LLM_PROVIDER", "openai")
    llm_service = get_llm_service(
        provider=provider,
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    )
