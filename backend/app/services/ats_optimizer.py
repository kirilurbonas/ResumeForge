"""ATS optimizer service for keyword matching and optimization."""

import re
from typing import List, Dict, Set
from app.models.resume_model import Resume


class ATSOptimizer:
    """Optimize resume for ATS (Applicant Tracking System) compatibility."""
    
    def __init__(self):
        self.common_ats_keywords = [
            'leadership', 'management', 'communication', 'teamwork',
            'problem solving', 'analytical', 'strategic', 'project management',
            'agile', 'scrum', 'collaboration', 'innovation', 'results-driven'
        ]
    
    def optimize(self, resume: Resume, job_description: str = None) -> Dict:
        """
        Generate ATS optimization suggestions.
        
        Args:
            resume: Resume object to optimize
            job_description: Optional job description to match against
            
        Returns:
            Dictionary with optimization suggestions and score
        """
        suggestions = []
        
        # Formatting checks
        suggestions.extend(self._check_formatting(resume))
        
        # Keyword optimization
        if job_description:
            suggestions.extend(self._suggest_missing_keywords(resume, job_description))
            match_score = self._calculate_match_score(resume, job_description)
        else:
            match_score = None
        
        # General ATS improvements
        suggestions.extend(self._general_ats_suggestions(resume))
        
        return {
            'suggestions': suggestions,
            'match_score': match_score,
            'ats_friendly': self._is_ats_friendly(resume)
        }
    
    def _check_formatting(self, resume: Resume) -> List[str]:
        """Check for ATS-friendly formatting."""
        suggestions = []
        
        # Check for tables (not ATS-friendly)
        if resume.raw_text:
            if '|' in resume.raw_text or '\t' in resume.raw_text:
                suggestions.append("Avoid using tables - ATS systems may not parse them correctly")
        
        # Check for standard fonts
        # Note: This is a simplified check - actual font detection would require parsing the document
        suggestions.append("Use standard fonts (Arial, Calibri, Times New Roman) for better ATS compatibility")
        
        # Check for proper section headers
        section_headers = ['experience', 'education', 'skills', 'summary']
        text_lower = (resume.raw_text or '').lower()
        found_headers = [h for h in section_headers if h in text_lower]
        
        if len(found_headers) < 3:
            suggestions.append("Ensure clear section headers (Experience, Education, Skills)")
        
        return suggestions
    
    def _suggest_missing_keywords(self, resume: Resume, job_description: str) -> List[str]:
        """Suggest missing keywords from job description."""
        suggestions = []
        
        # Extract keywords from job description
        job_keywords = self._extract_keywords(job_description)
        resume_text = (resume.raw_text or '').lower()
        
        # Find missing important keywords
        missing_keywords = []
        for keyword in job_keywords:
            if keyword.lower() not in resume_text:
                missing_keywords.append(keyword)
        
        if missing_keywords:
            top_missing = missing_keywords[:5]  # Top 5 missing
            suggestions.append(
                f"Consider adding these keywords from the job description: {', '.join(top_missing)}"
            )
        
        return suggestions
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        # Extract capitalized words and important phrases
        keywords = set()
        
        # Extract capitalized words (likely important terms)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
        keywords.update([w.lower() for w in capitalized if w.lower() not in stop_words])
        
        # Extract common technical terms
        tech_patterns = [
            r'\b\w+\s+(?:development|engineering|management|analysis|design)\b',
            r'\b(?:Python|JavaScript|Java|SQL|AWS|Docker|Kubernetes|React|Angular)\b',
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            keywords.update([m.lower() for m in matches])
        
        # Extract skills mentioned
        skills_section = re.search(r'skills?[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)', text, re.IGNORECASE | re.DOTALL)
        if skills_section:
            skills_text = skills_section.group(1)
            skills = re.findall(r'\b\w+\b', skills_text)
            keywords.update([s.lower() for s in skills if len(s) > 3])
        
        return list(keywords)[:20]  # Return top 20 keywords
    
    def _calculate_match_score(self, resume: Resume, job_description: str) -> int:
        """Calculate match score between resume and job description."""
        job_keywords = set(self._extract_keywords(job_description))
        resume_text = (resume.raw_text or '').lower()
        
        # Count matching keywords
        matches = 0
        for keyword in job_keywords:
            if keyword.lower() in resume_text:
                matches += 1
        
        # Calculate percentage match
        if len(job_keywords) > 0:
            score = int((matches / len(job_keywords)) * 100)
        else:
            score = 0
        
        return min(100, score)
    
    def _general_ats_suggestions(self, resume: Resume) -> List[str]:
        """General ATS optimization suggestions."""
        suggestions = []
        
        # Check for quantifiable achievements
        quantifiable_count = 0
        if resume.raw_text:
            patterns = [r'\d+%', r'\$\d+', r'\d+\+']
            for pattern in patterns:
                quantifiable_count += len(re.findall(pattern, resume.raw_text))
        
        if quantifiable_count < 3:
            suggestions.append("Add more quantifiable achievements (numbers, percentages, metrics)")
        
        # Check for action verbs
        action_verbs = ['developed', 'implemented', 'managed', 'led', 'created', 'improved']
        verb_count = sum(1 for verb in action_verbs if verb in (resume.raw_text or '').lower())
        
        if verb_count < 5:
            suggestions.append("Use more strong action verbs (developed, implemented, managed, led, etc.)")
        
        # Check contact info completeness
        if not resume.contact_info.email:
            suggestions.append("Ensure email address is included")
        
        if not resume.contact_info.phone:
            suggestions.append("Ensure phone number is included")
        
        # Check skills section
        if len(resume.skills) < 5:
            suggestions.append("List at least 5-10 relevant skills")
        
        return suggestions
    
    def _is_ats_friendly(self, resume: Resume) -> bool:
        """Check if resume is ATS-friendly."""
        # Basic checks
        has_email = resume.contact_info.email is not None
        has_phone = resume.contact_info.phone is not None
        has_experience = len(resume.experience) > 0
        has_skills = len(resume.skills) >= 5
        
        # Check for problematic characters (tables, special formatting)
        has_tables = '|' in (resume.raw_text or '') or '\t' in (resume.raw_text or '')
        
        return has_email and has_phone and has_experience and has_skills and not has_tables
