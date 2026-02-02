"""Text processing utilities."""

import re
from typing import List, Dict


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\;\:\-\'\"\(\)]', '', text)
    return text.strip()


def extract_email(text: str) -> str:
    """Extract email address from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None


def extract_phone(text: str) -> str:
    """Extract phone number from text."""
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
        r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
    ]
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    return None


def extract_linkedin(text: str) -> str:
    """Extract LinkedIn URL from text."""
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
    if matches:
        return f"https://{matches[0]}"
    return None


def extract_skills(text: str, common_skills: List[str] = None) -> List[str]:
    """Extract skills from text."""
    if common_skills is None:
        common_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'SQL', 'React', 'Node.js',
            'AWS', 'Docker', 'Kubernetes', 'Git', 'Linux', 'Machine Learning',
            'Data Science', 'Agile', 'Scrum', 'Project Management'
        ]
    
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return found_skills


def split_into_sections(text: str) -> Dict[str, str]:
    """Split resume text into sections."""
    sections = {}
    
    # Common section headers
    section_patterns = {
        'summary': r'(?:summary|profile|objective|about)\s*:?\s*\n',
        'experience': r'(?:experience|work\s+experience|employment|professional\s+experience)\s*:?\s*\n',
        'education': r'(?:education|academic|qualifications)\s*:?\s*\n',
        'skills': r'(?:skills|technical\s+skills|competencies)\s*:?\s*\n',
        'certifications': r'(?:certifications|certificates|credentials)\s*:?\s*\n',
        'projects': r'(?:projects|portfolio)\s*:?\s*\n',
    }
    
    current_section = 'header'
    current_text = []
    lines = text.split('\n')
    
    for line in lines:
        line_upper = line.upper().strip()
        matched = False
        
        for section_name, pattern in section_patterns.items():
            if re.search(pattern, line_upper):
                if current_section != 'header':
                    sections[current_section] = '\n'.join(current_text)
                current_section = section_name
                current_text = []
                matched = True
                break
        
        if not matched:
            current_text.append(line)
    
    # Add the last section
    if current_text:
        sections[current_section] = '\n'.join(current_text)
    
    return sections
