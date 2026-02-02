"""Job matcher service for resume-job matching."""

from typing import Dict
from app.models.resume_model import Resume
from app.services.skills_analyzer import SkillsAnalyzer
from app.services.ats_optimizer import ATSOptimizer


class JobMatcher:
    """Match resume to job description."""
    
    def __init__(self):
        self.skills_analyzer = SkillsAnalyzer()
        self.ats_optimizer = ATSOptimizer()
    
    def match(self, resume: Resume, job_description: str) -> Dict:
        """
        Match resume to job description and provide insights.
        
        Args:
            resume: Resume object
            job_description: Job description text
            
        Returns:
            Dictionary with match analysis
        """
        # Skills gap analysis
        skills_analysis = self.skills_analyzer.analyze_gaps(resume, job_description)
        
        # ATS optimization with job description
        ats_analysis = self.ats_optimizer.optimize(resume, job_description)
        
        # Overall match score
        overall_score = self._calculate_overall_score(skills_analysis, ats_analysis)
        
        return {
            'overall_match_score': overall_score,
            'skills_analysis': skills_analysis,
            'ats_analysis': ats_analysis,
            'recommendations': self._generate_recommendations(skills_analysis, ats_analysis)
        }
    
    def _calculate_overall_score(self, skills_analysis: Dict, ats_analysis: Dict) -> int:
        """Calculate overall match score."""
        skills_score = skills_analysis.get('match_percentage', 0)
        ats_score = ats_analysis.get('match_score', 0) or 0
        
        # Weighted average (60% skills, 40% ATS)
        overall = (skills_score * 0.6) + (ats_score * 0.4)
        return round(overall)
    
    def _generate_recommendations(self, skills_analysis: Dict, ats_analysis: Dict) -> list[str]:
        """Generate recommendations for improving match."""
        recommendations = []
        
        # Skills recommendations
        if skills_analysis['match_percentage'] < 70:
            recommendations.append("Add more skills from the job description to improve your match")
        
        missing_skills = skills_analysis.get('missing_skills', [])
        if missing_skills:
            top_missing = missing_skills[:3]
            recommendations.append(f"Prioritize adding these skills: {', '.join(top_missing)}")
        
        # ATS recommendations
        ats_suggestions = ats_analysis.get('suggestions', [])
        if ats_suggestions:
            recommendations.extend(ats_suggestions[:2])  # Top 2 ATS suggestions
        
        return recommendations
