"""Resume analyzer service for strengths/weaknesses detection and metrics."""

import re
from typing import List, Dict
from app.models.resume_model import Resume


class ResumeAnalyzer:
    """Analyze resume quality and provide insights."""
    
    def __init__(self):
        self.strong_action_verbs = [
            'achieved', 'improved', 'increased', 'decreased', 'reduced',
            'developed', 'created', 'designed', 'implemented', 'managed',
            'led', 'coordinated', 'executed', 'delivered', 'optimized',
            'enhanced', 'streamlined', 'established', 'launched', 'built'
        ]
        
        self.weak_action_verbs = [
            'worked', 'did', 'made', 'helped', 'assisted', 'responsible for'
        ]
    
    def analyze(self, resume: Resume) -> Dict:
        """
        Perform comprehensive analysis of resume.
        
        Returns:
            Dictionary with analysis results including:
            - ats_score: ATS compatibility score (0-100)
            - strengths: List of strengths
            - weaknesses: List of weaknesses
            - metrics: Various metrics about the resume
            - keyword_analysis: Keyword frequency and importance
        """
        strengths = []
        weaknesses = []
        metrics = self._calculate_metrics(resume)
        
        # Analyze strengths
        strengths.extend(self._analyze_quantifiable_achievements(resume))
        strengths.extend(self._analyze_action_verbs(resume))
        strengths.extend(self._analyze_structure(resume))
        
        # Analyze weaknesses
        weaknesses.extend(self._analyze_missing_elements(resume))
        weaknesses.extend(self._analyze_weak_language(resume))
        weaknesses.extend(self._analyze_formatting_issues(resume))
        
        # Calculate ATS score
        ats_score = self._calculate_ats_score(resume, metrics)
        
        # Keyword analysis
        keyword_analysis = self._analyze_keywords(resume)
        
        return {
            'ats_score': ats_score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'metrics': metrics,
            'keyword_analysis': keyword_analysis
        }
    
    def _calculate_metrics(self, resume: Resume) -> Dict:
        """Calculate various metrics about the resume."""
        total_experience_years = 0
        for exp in resume.experience:
            try:
                start_year = int(exp.start_date[:4]) if len(exp.start_date) >= 4 else 0
                end_year = int(exp.end_date[:4]) if exp.end_date and len(exp.end_date) >= 4 else 2024
                if start_year > 0:
                    total_experience_years += (end_year - start_year)
            except:
                pass
        
        # Count quantifiable achievements
        quantifiable_count = 0
        for exp in resume.experience:
            for desc in exp.description:
                if re.search(r'\d+%|\d+\+|\$\d+|\d+\s*(years|months|people|projects)', desc, re.IGNORECASE):
                    quantifiable_count += 1
        
        # Calculate text length
        text_length = len(resume.raw_text or '')
        
        return {
            'total_experience_years': total_experience_years,
            'number_of_positions': len(resume.experience),
            'number_of_skills': len(resume.skills),
            'number_of_certifications': len(resume.certifications),
            'has_summary': resume.summary is not None,
            'quantifiable_achievements': quantifiable_count,
            'text_length': text_length,
            'average_description_length': self._avg_description_length(resume)
        }
    
    def _avg_description_length(self, resume: Resume) -> float:
        """Calculate average description length."""
        total_length = 0
        total_count = 0
        for exp in resume.experience:
            for desc in exp.description:
                total_length += len(desc)
                total_count += 1
        return total_length / total_count if total_count > 0 else 0
    
    def _analyze_quantifiable_achievements(self, resume: Resume) -> List[str]:
        """Identify quantifiable achievements."""
        strengths = []
        quantifiable_patterns = [
            r'\d+%',
            r'\$\d+',
            r'\d+\+',
            r'\d+\s*(years|months|people|projects|clients|users)',
        ]
        
        quantifiable_count = 0
        for exp in resume.experience:
            for desc in exp.description:
                for pattern in quantifiable_patterns:
                    if re.search(pattern, desc, re.IGNORECASE):
                        quantifiable_count += 1
                        break
        
        if quantifiable_count >= 3:
            strengths.append(f"Strong use of quantifiable achievements ({quantifiable_count} found)")
        elif quantifiable_count > 0:
            strengths.append(f"Some quantifiable achievements present ({quantifiable_count} found)")
        
        return strengths
    
    def _analyze_action_verbs(self, resume: Resume) -> List[str]:
        """Analyze use of strong action verbs."""
        strengths = []
        strong_count = 0
        weak_count = 0
        
        for exp in resume.experience:
            for desc in exp.description:
                desc_lower = desc.lower()
                for verb in self.strong_action_verbs:
                    if verb in desc_lower:
                        strong_count += 1
                for verb in self.weak_action_verbs:
                    if verb in desc_lower:
                        weak_count += 1
        
        if strong_count > weak_count * 2:
            strengths.append("Excellent use of strong action verbs")
        elif strong_count > weak_count:
            strengths.append("Good use of action verbs")
        
        return strengths
    
    def _analyze_structure(self, resume: Resume) -> List[str]:
        """Analyze resume structure."""
        strengths = []
        
        if resume.summary:
            strengths.append("Professional summary present")
        
        if len(resume.experience) >= 2:
            strengths.append("Adequate work experience listed")
        
        if len(resume.skills) >= 5:
            strengths.append("Good variety of skills")
        
        if resume.contact_info.email:
            strengths.append("Contact information complete")
        
        return strengths
    
    def _analyze_missing_elements(self, resume: Resume) -> List[str]:
        """Identify missing important elements."""
        weaknesses = []
        
        if not resume.summary:
            weaknesses.append("Missing professional summary")
        
        if len(resume.experience) == 0:
            weaknesses.append("No work experience listed")
        
        if len(resume.skills) < 5:
            weaknesses.append("Limited skills listed (consider adding more)")
        
        if not resume.contact_info.email:
            weaknesses.append("Missing email address")
        
        if not resume.contact_info.phone:
            weaknesses.append("Missing phone number")
        
        return weaknesses
    
    def _analyze_weak_language(self, resume: Resume) -> List[str]:
        """Identify weak language patterns."""
        weaknesses = []
        weak_count = 0
        
        for exp in resume.experience:
            for desc in exp.description:
                desc_lower = desc.lower()
                if any(verb in desc_lower for verb in self.weak_action_verbs):
                    weak_count += 1
        
        if weak_count > 3:
            weaknesses.append("Too many weak action verbs (consider using stronger verbs)")
        
        # Check for vague descriptions
        vague_words = ['various', 'many', 'some', 'several', 'assisted with']
        vague_count = 0
        for exp in resume.experience:
            for desc in exp.description:
                if any(word in desc.lower() for word in vague_words):
                    vague_count += 1
        
        if vague_count > 2:
            weaknesses.append("Vague language detected (be more specific)")
        
        return weaknesses
    
    def _analyze_formatting_issues(self, resume: Resume) -> List[str]:
        """Identify potential formatting issues."""
        weaknesses = []
        
        # Check text length
        if resume.raw_text:
            text_length = len(resume.raw_text)
            if text_length > 2000:
                weaknesses.append("Resume may be too long (consider condensing)")
            elif text_length < 300:
                weaknesses.append("Resume may be too short (add more detail)")
        
        # Check for consistent formatting in descriptions
        desc_lengths = []
        for exp in resume.experience:
            for desc in exp.description:
                desc_lengths.append(len(desc))
        
        if desc_lengths:
            avg_length = sum(desc_lengths) / len(desc_lengths)
            if any(abs(len(d) - avg_length) > avg_length * 0.5 for d in desc_lengths):
                weaknesses.append("Inconsistent description lengths (aim for consistency)")
        
        return weaknesses
    
    def _calculate_ats_score(self, resume: Resume, metrics: Dict) -> int:
        """Calculate ATS compatibility score (0-100)."""
        score = 0
        
        # Contact info (20 points)
        if resume.contact_info.email:
            score += 10
        if resume.contact_info.phone:
            score += 10
        
        # Structure (30 points)
        if resume.summary:
            score += 10
        if len(resume.experience) > 0:
            score += 10
        if len(resume.skills) >= 5:
            score += 10
        
        # Content quality (30 points)
        if metrics['quantifiable_achievements'] >= 3:
            score += 15
        elif metrics['quantifiable_achievements'] > 0:
            score += 8
        
        if metrics['average_description_length'] > 50:
            score += 15
        
        # Formatting (20 points)
        text_length = metrics['text_length']
        if 500 <= text_length <= 2000:
            score += 20
        elif 300 <= text_length < 500 or 2000 < text_length <= 3000:
            score += 10
        
        return min(100, score)
    
    def _analyze_keywords(self, resume: Resume) -> Dict:
        """Analyze keyword frequency and importance."""
        if not resume.raw_text:
            return {}
        
        text_lower = resume.raw_text.lower()
        
        # Common resume keywords
        important_keywords = [
            'experience', 'skills', 'education', 'certification',
            'project', 'achievement', 'leadership', 'management',
            'development', 'implementation', 'optimization', 'analysis'
        ]
        
        keyword_freq = {}
        for keyword in important_keywords:
            count = text_lower.count(keyword)
            if count > 0:
                keyword_freq[keyword] = count
        
        # Extract skills as keywords
        skill_keywords = {}
        for skill in resume.skills:
            skill_name_lower = skill.name.lower()
            count = text_lower.count(skill_name_lower)
            skill_keywords[skill.name] = count
        
        return {
            'important_keywords': keyword_freq,
            'skill_keywords': skill_keywords,
            'total_unique_keywords': len(keyword_freq) + len(skill_keywords)
        }
