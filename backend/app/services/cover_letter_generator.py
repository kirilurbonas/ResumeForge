"""Cover letter generation service."""

from typing import Optional, Dict
from app.models.resume_model import Resume
from app.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)


class CoverLetterGenerator:
    """Generate cover letters based on resume and job description."""
    
    def __init__(self):
        self.default_tone = "professional"
        self.default_length = "medium"  # short, medium, long
    
    def generate(
        self,
        resume: Resume,
        job_description: str,
        company_name: Optional[str] = None,
        tone: Optional[str] = None,
        length: Optional[str] = None
    ) -> Dict:
        """
        Generate a cover letter.
        
        Args:
            resume: Resume data
            job_description: Job description text
            company_name: Optional company name
            tone: Writing tone (professional, friendly, formal)
            length: Letter length (short, medium, long)
            
        Returns:
            Dictionary with cover letter content and metadata
        """
        tone = tone or self.default_tone
        length = length or self.default_length
        
        # Build prompt for LLM
        prompt = self._build_prompt(resume, job_description, company_name, tone, length)
        
        try:
            if llm_service and hasattr(llm_service, 'generate_text'):
                cover_letter_text = llm_service.generate_text(prompt)
            else:
                # Fallback template-based generation
                cover_letter_text = self._generate_template_based(resume, job_description, company_name, tone, length)
            
            return {
                "cover_letter": cover_letter_text,
                "tone": tone,
                "length": length,
                "company_name": company_name,
                "word_count": len(cover_letter_text.split())
            }
        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            # Fallback to template-based
            return {
                "cover_letter": self._generate_template_based(resume, job_description, company_name, tone, length),
                "tone": tone,
                "length": length,
                "company_name": company_name,
                "word_count": 0
            }
    
    def _build_prompt(
        self,
        resume: Resume,
        job_description: str,
        company_name: Optional[str],
        tone: str,
        length: str
    ) -> str:
        """Build LLM prompt for cover letter generation."""
        
        length_guidance = {
            "short": "Keep it concise, around 200-250 words",
            "medium": "Write a standard length cover letter, around 300-400 words",
            "long": "Write a detailed cover letter, around 500-600 words"
        }
        
        tone_guidance = {
            "professional": "Use a professional, confident tone",
            "friendly": "Use a warm, approachable tone while remaining professional",
            "formal": "Use a formal, traditional business letter tone"
        }
        
        prompt = f"""Write a {tone} cover letter for the following position.

{length_guidance.get(length, length_guidance['medium'])}
{tone_guidance.get(tone, tone_guidance['professional'])}

Job Description:
{job_description}

Candidate Information:
Name: {resume.contact_info.name}
Email: {resume.contact_info.email or 'Not provided'}
Summary: {resume.summary or 'Not provided'}
Years of Experience: {len(resume.experience)} positions
Key Skills: {', '.join([s.name for s in resume.skills[:10]])}

"""
        
        if company_name:
            prompt += f"Company: {company_name}\n"
        
        prompt += """
Write a compelling cover letter that:
1. Addresses the hiring manager (use "Dear Hiring Manager" if company name not provided)
2. Expresses genuine interest in the position
3. Highlights relevant experience and skills from the resume
4. Explains why the candidate is a good fit
5. Includes a strong closing statement

Cover Letter:"""
        
        return prompt
    
    def _generate_template_based(
        self,
        resume: Resume,
        job_description: str,
        company_name: Optional[str],
        tone: str,
        length: str
    ) -> str:
        """Generate cover letter using template when LLM is not available."""
        
        greeting = f"Dear Hiring Manager"
        if company_name:
            greeting = f"Dear {company_name} Hiring Team"
        
        # Extract key skills
        skills_list = ', '.join([s.name for s in resume.skills[:5]])
        
        # Build cover letter
        cover_letter = f"""{greeting},

I am writing to express my interest in the position. With {len(resume.experience)} years of professional experience, I am excited about the opportunity to contribute to your team.

{resume.summary or 'I bring a strong background in my field with proven experience.'}

My key qualifications include:
- {skills_list}
- Experience in {', '.join([exp.position for exp in resume.experience[:3]])}

I am particularly drawn to this role because it aligns with my career goals and allows me to leverage my skills in [relevant area].

Thank you for considering my application. I look forward to the opportunity to discuss how my experience and skills can contribute to your team.

Sincerely,
{resume.contact_info.name}
{resume.contact_info.email or ''}
"""
        
        return cover_letter
