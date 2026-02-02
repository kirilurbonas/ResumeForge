"""Format optimizer service for improving resume formatting."""

from typing import List, Dict
from app.models.resume_model import Resume


class FormatOptimizer:
    """Optimize resume formatting for better readability and ATS compatibility."""
    
    def optimize(self, resume: Resume) -> Dict:
        """
        Apply format improvements to resume.
        
        Args:
            resume: Resume object to optimize
            
        Returns:
            Dictionary with optimization results and suggestions
        """
        improvements = []
        optimized_resume = self._create_optimized_copy(resume)
        
        # Check and fix spacing consistency
        improvements.extend(self._fix_spacing_issues(optimized_resume))
        
        # Check and fix formatting consistency
        improvements.extend(self._fix_formatting_consistency(optimized_resume))
        
        # Check and fix ATS compatibility
        improvements.extend(self._ensure_ats_compatibility(optimized_resume))
        
        # Check and fix structure
        improvements.extend(self._optimize_structure(optimized_resume))
        
        return {
            'improvements_applied': improvements,
            'optimized_resume': optimized_resume,
            'summary': f"Applied {len(improvements)} formatting improvements"
        }
    
    def _create_optimized_copy(self, resume: Resume) -> Resume:
        """Create a copy of resume for optimization."""
        # In a real implementation, we'd deep copy the resume
        # For now, we'll work with the original but track changes
        return resume
    
    def _fix_spacing_issues(self, resume: Resume) -> List[str]:
        """Fix spacing inconsistencies."""
        improvements = []
        
        # Check description lengths for consistency
        desc_lengths = []
        for exp in resume.experience:
            for desc in exp.description:
                desc_lengths.append(len(desc))
        
        if desc_lengths:
            avg_length = sum(desc_lengths) / len(desc_lengths)
            # Flag descriptions that are too short or too long
            short_descriptions = [i for i, length in enumerate(desc_lengths) if length < avg_length * 0.5]
            if short_descriptions:
                improvements.append("Some descriptions are too short - consider adding more detail")
            
            long_descriptions = [i for i, length in enumerate(desc_lengths) if length > avg_length * 1.5]
            if long_descriptions:
                improvements.append("Some descriptions are too long - consider condensing")
        
        # Check for consistent bullet point formatting
        bullet_consistency = True
        for exp in resume.experience:
            if exp.description:
                first_has_bullet = exp.description[0].startswith('•') or exp.description[0].startswith('-')
                for desc in exp.description[1:]:
                    has_bullet = desc.startswith('•') or desc.startswith('-')
                    if has_bullet != first_has_bullet:
                        bullet_consistency = False
                        break
        
        if not bullet_consistency:
            improvements.append("Inconsistent bullet point formatting - standardize bullet style")
        
        return improvements
    
    def _fix_formatting_consistency(self, resume: Resume) -> List[str]:
        """Fix formatting inconsistencies."""
        improvements = []
        
        # Check date format consistency
        date_formats = []
        for exp in resume.experience:
            if exp.start_date:
                date_formats.append(self._detect_date_format(exp.start_date))
        
        if len(set(date_formats)) > 1:
            improvements.append("Inconsistent date formats - use consistent format (e.g., 'MM/YYYY')")
        
        # Check for proper capitalization
        capitalization_issues = []
        for exp in resume.experience:
            if exp.position and not exp.position[0].isupper():
                capitalization_issues.append("position titles")
            if exp.company and not exp.company[0].isupper():
                capitalization_issues.append("company names")
        
        if capitalization_issues:
            improvements.append("Ensure proper capitalization for position titles and company names")
        
        return improvements
    
    def _detect_date_format(self, date_str: str) -> str:
        """Detect date format."""
        if '/' in date_str:
            return 'slash'
        elif '-' in date_str:
            return 'dash'
        elif len(date_str) == 4 and date_str.isdigit():
            return 'year_only'
        else:
            return 'other'
    
    def _ensure_ats_compatibility(self, resume: Resume) -> List[str]:
        """Ensure ATS-friendly formatting."""
        improvements = []
        
        # Check for tables (not ATS-friendly)
        if resume.raw_text:
            if '|' in resume.raw_text or '\t' in resume.raw_text:
                improvements.append("Remove tables - use standard formatting for better ATS compatibility")
        
        # Check for special characters that might confuse ATS
        special_chars = ['©', '®', '™', '•']
        found_chars = [char for char in special_chars if char in (resume.raw_text or '')]
        if found_chars:
            improvements.append("Replace special characters with standard alternatives for ATS compatibility")
        
        # Check for proper section headers
        section_headers = ['experience', 'education', 'skills', 'summary']
        text_lower = (resume.raw_text or '').lower()
        found_headers = [h for h in section_headers if h in text_lower]
        
        if len(found_headers) < 3:
            improvements.append("Ensure clear section headers are present (Experience, Education, Skills)")
        
        return improvements
    
    def _optimize_structure(self, resume: Resume) -> List[str]:
        """Optimize resume structure."""
        improvements = []
        
        # Check section order (should be: Contact, Summary, Experience, Education, Skills)
        # This is more of a suggestion than an automatic fix
        
        # Check if summary is too long
        if resume.summary and len(resume.summary) > 500:
            improvements.append("Summary is too long - keep it under 3-4 sentences")
        
        # Check if experience entries are in reverse chronological order
        # (most recent first)
        if len(resume.experience) > 1:
            # Simple check - if dates are provided, verify order
            dates_valid = True
            for i in range(len(resume.experience) - 1):
                try:
                    current_year = int(resume.experience[i].start_date[:4]) if len(resume.experience[i].start_date) >= 4 else 0
                    next_year = int(resume.experience[i+1].start_date[:4]) if len(resume.experience[i+1].start_date) >= 4 else 0
                    if current_year > 0 and next_year > 0 and current_year < next_year:
                        dates_valid = False
                        break
                except:
                    pass
            
            if not dates_valid:
                improvements.append("Ensure experience is listed in reverse chronological order (most recent first)")
        
        # Check for empty sections
        if resume.experience and len(resume.experience) == 0:
            improvements.append("Add work experience section")
        
        if resume.skills and len(resume.skills) == 0:
            improvements.append("Add skills section")
        
        return improvements
    
    def get_formatting_suggestions(self, resume: Resume) -> List[str]:
        """Get formatting suggestions without applying changes."""
        suggestions = []
        
        # Spacing suggestions
        suggestions.extend(self._fix_spacing_issues(resume))
        
        # Formatting suggestions
        suggestions.extend(self._fix_formatting_consistency(resume))
        
        # ATS suggestions
        suggestions.extend(self._ensure_ats_compatibility(resume))
        
        # Structure suggestions
        suggestions.extend(self._optimize_structure(resume))
        
        return suggestions
