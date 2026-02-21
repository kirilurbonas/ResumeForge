"""Interview question preparation service."""

from typing import List, Dict, Optional
from app.models.resume_model import Resume
from app.services.llm_service import llm_service
import logging
import json

logger = logging.getLogger(__name__)


class InterviewPrepService:
    """Generate interview questions and preparation materials."""
    
    def __init__(self):
        self.common_questions = [
            "Tell me about yourself.",
            "Why do you want to work here?",
            "What are your greatest strengths?",
            "What are your weaknesses?",
            "Where do you see yourself in 5 years?",
            "Why should we hire you?",
            "Tell me about a challenge you faced and how you overcame it.",
            "How do you handle stress and pressure?",
            "What are your salary expectations?",
            "Do you have any questions for us?"
        ]
    
    def generate_questions(
        self,
        resume: Resume,
        job_description: str,
        question_types: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate interview questions based on resume and job description.
        
        Args:
            resume: Resume data
            job_description: Job description text
            question_types: Types of questions to generate (behavioral, technical, situational, etc.)
            
        Returns:
            Dictionary with categorized questions and suggested answers
        """
        question_types = question_types or ["behavioral", "technical", "situational"]
        
        try:
            if llm_service:
                questions = self._generate_with_llm(resume, job_description, question_types)
            else:
                questions = self._generate_template_based(resume, job_description, question_types)
            
            return {
                "questions": questions,
                "resume_id": resume.id,
                "total_questions": sum(len(q['questions']) for q in questions.values())
            }
        except Exception as e:
            logger.error(f"Error generating interview questions: {e}")
            return {
                "questions": self._generate_template_based(resume, job_description, question_types),
                "resume_id": resume.id,
                "total_questions": 0
            }
    
    def generate_answer_suggestions(
        self,
        resume: Resume,
        question: str,
        job_description: Optional[str] = None
    ) -> Dict:
        """
        Generate suggested answers for a specific interview question.
        
        Args:
            resume: Resume data
            question: Interview question
            job_description: Optional job description for context
            
        Returns:
            Dictionary with suggested answer and tips
        """
        try:
            if llm_service and hasattr(llm_service, 'generate_text'):
                answer = self._generate_answer_with_llm(resume, question, job_description)
            else:
                answer = self._generate_answer_template(resume, question)
            
            return {
                "question": question,
                "suggested_answer": answer["answer"],
                "tips": answer.get("tips", []),
                "key_points": answer.get("key_points", [])
            }
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return {
                "question": question,
                "suggested_answer": "Prepare a thoughtful answer based on your experience.",
                "tips": ["Be specific", "Use examples", "Stay positive"],
                "key_points": []
            }
    
    def _generate_with_llm(
        self,
        resume: Resume,
        job_description: str,
        question_types: List[str]
    ) -> Dict:
        """Generate questions using LLM."""
        prompt = f"""Generate interview questions for the following candidate and position.

Job Description:
{job_description}

Candidate Summary:
{resume.summary or 'See resume for details'}

Key Skills: {', '.join([s.name for s in resume.skills[:10]])}
Experience: {len(resume.experience)} positions

Generate {len(question_types)} categories of questions:
{', '.join(question_types)}

For each category, provide 3-5 relevant questions. Format as JSON with categories as keys and arrays of questions as values.
"""
        
        try:
            if llm_service and hasattr(llm_service, 'generate_text'):
                response = llm_service.generate_text(prompt)
                # Try to parse JSON response
                questions = json.loads(response)
                return questions
        except:
            pass
        # Fallback to template
        return self._generate_template_based(resume, job_description, question_types)
    
    def _generate_template_based(
        self,
        resume: Resume,
        job_description: str,
        question_types: List[str]
    ) -> Dict:
        """Generate questions using templates."""
        questions = {}
        
        if "behavioral" in question_types:
            questions["behavioral"] = [
                "Tell me about a time you had to work under pressure.",
                "Describe a situation where you had to solve a complex problem.",
                "Give an example of when you worked effectively in a team.",
                "Tell me about a time you had to adapt to a significant change."
            ]
        
        if "technical" in question_types:
            skills = [s.name for s in resume.skills[:5]]
            questions["technical"] = [
                f"Explain your experience with {skills[0] if skills else 'your primary skill'}.",
                "Describe a technical project you're particularly proud of.",
                "How do you stay current with industry trends?",
                "Walk me through your approach to debugging a complex issue."
            ]
        
        if "situational" in question_types:
            questions["situational"] = [
                "What would you do if you disagreed with your manager?",
                "How would you handle a tight deadline with limited resources?",
                "Describe how you would onboard a new team member.",
                "What would you do if a project was behind schedule?"
            ]
        
        if "general" in question_types:
            questions["general"] = self.common_questions[:5]
        
        return questions
    
    def _generate_answer_with_llm(
        self,
        resume: Resume,
        question: str,
        job_description: Optional[str]
    ) -> Dict:
        """Generate answer using LLM."""
        prompt = f"""Provide a suggested answer for this interview question based on the candidate's resume.

Question: {question}

Candidate Summary: {resume.summary or 'See resume'}
Key Experience: {', '.join([exp.position for exp in resume.experience[:3]])}
Key Skills: {', '.join([s.name for s in resume.skills[:5]])}
"""
        
        if job_description:
            prompt += f"\nJob Description Context: {job_description[:500]}"
        
        prompt += "\n\nProvide:\n1. A suggested answer (2-3 paragraphs)\n2. Key points to mention\n3. Tips for answering"
        
        try:
            if llm_service and hasattr(llm_service, 'generate_text'):
                response = llm_service.generate_text(prompt)
                return {
                    "answer": response,
                    "key_points": [],
                    "tips": ["Be specific", "Use examples from your experience"]
                }
        except:
            pass
        return self._generate_answer_template(resume, question)
    
    def _generate_answer_template(self, resume: Resume, question: str) -> Dict:
        """Generate answer using template."""
        return {
            "answer": f"Based on my experience as {resume.experience[0].position if resume.experience else 'a professional'}, I would approach this question by highlighting my relevant skills and experience. {resume.summary or 'I bring strong qualifications to this role.'}",
            "key_points": [
                "Highlight relevant experience",
                "Use specific examples",
                "Connect to the role"
            ],
            "tips": [
                "Prepare specific examples",
                "Use the STAR method (Situation, Task, Action, Result)",
                "Be concise but thorough"
            ]
        }
