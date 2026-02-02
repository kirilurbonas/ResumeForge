"""Skills analyzer service for gap analysis."""

from typing import List, Dict, Set
from app.models.resume_model import Resume


class SkillsAnalyzer:
    """Analyze skills and identify gaps."""
    
    def analyze_gaps(self, resume: Resume, job_description: str) -> Dict:
        """
        Analyze skills gap between resume and job description.
        
        Args:
            resume: Resume object
            job_description: Job description text
            
        Returns:
            Dictionary with gap analysis
        """
        resume_skills = {skill.name.lower() for skill in resume.skills}
        job_skills = self._extract_skills_from_job(job_description)
        
        # Find matching skills
        matching_skills = resume_skills.intersection(job_skills)
        
        # Find missing skills
        missing_skills = job_skills - resume_skills
        
        # Find extra skills (in resume but not in job)
        extra_skills = resume_skills - job_skills
        
        # Calculate match percentage
        match_percentage = (len(matching_skills) / len(job_skills) * 100) if job_skills else 0
        
        return {
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'extra_skills': list(extra_skills),
            'match_percentage': round(match_percentage, 2),
            'suggestions': self._generate_suggestions(matching_skills, missing_skills, match_percentage)
        }
    
    def _extract_skills_from_job(self, job_description: str) -> Set[str]:
        """Extract skills mentioned in job description."""
        skills = set()
        job_lower = job_description.lower()
        
        # Common technical skills
        tech_skills = [
            'python', 'javascript', 'java', 'c++', 'sql', 'react', 'node.js',
            'aws', 'docker', 'kubernetes', 'git', 'linux', 'machine learning',
            'data science', 'agile', 'scrum', 'project management', 'mongodb',
            'postgresql', 'redis', 'kafka', 'rest api', 'graphql', 'typescript',
            'angular', 'vue.js', 'html', 'css', 'tensorflow', 'pytorch'
        ]
        
        # Check for technical skills
        for skill in tech_skills:
            if skill in job_lower:
                skills.add(skill)
        
        # Extract from "Skills" or "Requirements" section
        skills_section_patterns = [
            r'skills?[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)',
            r'requirements?[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)',
            r'qualifications?[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)',
        ]
        
        import re
        for pattern in skills_section_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Extract individual skills
                skill_items = re.findall(r'\b\w+(?:\s+\w+)?\b', match)
                for item in skill_items:
                    if len(item) > 3:  # Filter out very short words
                        skills.add(item.lower())
        
        return skills
    
    def _generate_suggestions(self, matching: Set[str], missing: Set[str], match_percentage: float) -> List[str]:
        """Generate suggestions based on gap analysis."""
        suggestions = []
        
        if match_percentage < 50:
            suggestions.append("Low skill match - consider adding more relevant skills from the job description")
        elif match_percentage < 75:
            suggestions.append("Moderate skill match - add a few more matching skills to improve your fit")
        else:
            suggestions.append("Good skill match - your skills align well with the job requirements")
        
        if missing:
            top_missing = list(missing)[:5]
            suggestions.append(f"Consider highlighting or adding these skills: {', '.join(top_missing)}")
        
        if len(matching) > 0:
            suggestions.append(f"You have {len(matching)} matching skills - make sure these are prominently featured")
        
        return suggestions
