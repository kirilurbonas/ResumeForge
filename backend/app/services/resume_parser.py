"""Resume parser service to extract structured data from PDF/DOCX files."""

import io
import re
import uuid
from datetime import datetime
from typing import Dict, Optional
import PyPDF2
from docx import Document
from app.models.resume_model import Resume, ContactInfo, Experience, Education, Skill, Certification
from app.utils.text_processor import (
    clean_text, extract_email, extract_phone, extract_linkedin,
    extract_skills, split_into_sections
)


class ResumeParser:
    """Parse resumes from PDF and DOCX files."""
    
    def __init__(self):
        self.common_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'SQL', 'React', 'Node.js',
            'Angular', 'Vue.js', 'TypeScript', 'HTML', 'CSS', 'AWS', 'Docker',
            'Kubernetes', 'Git', 'Linux', 'Machine Learning', 'Data Science',
            'Agile', 'Scrum', 'Project Management', 'TensorFlow', 'PyTorch',
            'MongoDB', 'PostgreSQL', 'Redis', 'Kafka', 'REST API', 'GraphQL'
        ]
    
    def parse(self, file_content: bytes, filename: str) -> Resume:
        """
        Parse resume file and extract structured data.
        
        Args:
            file_content: Raw file content bytes
            filename: Original filename
            
        Returns:
            Resume object with parsed data
        """
        # Determine file type
        if filename.lower().endswith('.pdf'):
            text = self._extract_from_pdf(file_content)
        elif filename.lower().endswith(('.docx', '.doc')):
            text = self._extract_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file format: {filename}")
        
        # Parse structured data
        resume_id = str(uuid.uuid4())
        contact_info = self._extract_contact_info(text)
        sections = split_into_sections(text)
        
        resume = Resume(
            id=resume_id,
            filename=filename,
            uploaded_at=datetime.now(),
            contact_info=contact_info,
            summary=self._extract_summary(sections.get('summary', '')),
            experience=self._extract_experience(sections.get('experience', '')),
            education=self._extract_education(sections.get('education', '')),
            skills=self._extract_skills(sections.get('skills', '') + ' ' + text),
            certifications=self._extract_certifications(sections.get('certifications', '')),
            raw_text=text
        )
        
        return resume
    
    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file."""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return clean_text(text)
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file."""
        try:
            doc_file = io.BytesIO(file_content)
            doc = Document(doc_file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return clean_text(text)
        except Exception as e:
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")
    
    def _extract_contact_info(self, text: str) -> ContactInfo:
        """Extract contact information from text."""
        # Get first few lines (usually contains contact info)
        lines = text.split('\n')[:10]
        header_text = '\n'.join(lines)
        
        # Extract name (usually first line or first two words)
        name = lines[0].strip() if lines else "Unknown"
        if len(name.split()) > 4:  # Probably not just a name
            name = ' '.join(name.split()[:2])
        
        email = extract_email(text)
        phone = extract_phone(text)
        linkedin = extract_linkedin(text)
        
        # Try to extract location (look for city, state patterns)
        location = None
        location_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z]{2})',  # City, State
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z][a-z]+)',  # City, Country
        ]
        for pattern in location_patterns:
            matches = re.findall(pattern, text[:500])
            if matches:
                location = ', '.join(matches[0])
                break
        
        return ContactInfo(
            name=name,
            email=email,
            phone=phone,
            location=location,
            linkedin=linkedin
        )
    
    def _extract_summary(self, summary_text: str) -> Optional[str]:
        """Extract summary/professional summary."""
        if not summary_text:
            return None
        
        # Clean and limit length
        summary = clean_text(summary_text)
        if len(summary) > 500:
            summary = summary[:500] + "..."
        
        return summary if summary else None
    
    def _extract_experience(self, experience_text: str) -> list[Experience]:
        """Extract work experience."""
        experiences = []
        if not experience_text:
            return experiences
        
        # Split by common patterns (company names, dates)
        # This is a simplified parser - can be enhanced
        lines = experience_text.split('\n')
        current_exp = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for date patterns (e.g., "2020 - 2023" or "Jan 2020 - Present")
            date_pattern = r'(\d{4}|\w+\s+\d{4})\s*[-–—]\s*(\d{4}|Present|Current)'
            date_match = re.search(date_pattern, line, re.IGNORECASE)
            
            if date_match:
                # Save previous experience if exists
                if current_exp:
                    experiences.append(current_exp)
                
                # Start new experience
                start_date = date_match.group(1)
                end_date = date_match.group(2) if date_match.group(2) not in ['Present', 'Current'] else None
                current = date_match.group(2) in ['Present', 'Current']
                
                # Extract company and position (usually before or after date)
                parts = re.split(date_pattern, line)
                company_pos = parts[0].strip() if parts else line
                
                # Try to split company and position
                if ' at ' in company_pos.lower():
                    parts = company_pos.split(' at ', 1)
                    position = parts[0].strip()
                    company = parts[1].strip()
                elif ' - ' in company_pos:
                    parts = company_pos.split(' - ', 1)
                    position = parts[0].strip()
                    company = parts[1].strip()
                else:
                    position = company_pos
                    company = "Unknown"
                
                current_exp = Experience(
                    company=company,
                    position=position,
                    start_date=start_date,
                    end_date=end_date,
                    current=current,
                    description=[]
                )
            elif current_exp:
                # Add to description
                if line and not re.match(r'^\d', line):  # Skip lines starting with numbers
                    current_exp.description.append(line)
        
        # Add last experience
        if current_exp:
            experiences.append(current_exp)
        
        return experiences
    
    def _extract_education(self, education_text: str) -> list[Education]:
        """Extract education information."""
        educations = []
        if not education_text:
            return educations
        
        lines = education_text.split('\n')
        current_edu = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for degree patterns
            degree_patterns = [
                r'(Bachelor|Master|PhD|Doctorate|Associate)\s+(?:of|in)\s+(\w+)',
                r'(B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|Ph\.?D\.?)\s+(?:in\s+)?(\w+)',
            ]
            
            degree_match = None
            for pattern in degree_patterns:
                degree_match = re.search(pattern, line, re.IGNORECASE)
                if degree_match:
                    break
            
            if degree_match or 'University' in line or 'College' in line:
                if current_edu:
                    educations.append(current_edu)
                
                # Extract institution and degree
                if 'University' in line or 'College' in line:
                    parts = line.split(',')
                    institution = parts[0].strip()
                    degree = ' '.join(parts[1:]).strip() if len(parts) > 1 else "Degree"
                else:
                    institution = line
                    degree = degree_match.group(0) if degree_match else "Degree"
                
                # Look for dates
                date_pattern = r'(\d{4})\s*[-–—]\s*(\d{4}|Present)'
                date_match = re.search(date_pattern, line)
                start_date = date_match.group(1) if date_match else "Unknown"
                end_date = date_match.group(2) if date_match and date_match.group(2) != 'Present' else None
                
                current_edu = Education(
                    institution=institution,
                    degree=degree,
                    start_date=start_date,
                    end_date=end_date
                )
            elif current_edu:
                # Look for GPA
                gpa_match = re.search(r'GPA[:\s]+([\d\.]+)', line, re.IGNORECASE)
                if gpa_match:
                    current_edu.gpa = gpa_match.group(1)
        
        if current_edu:
            educations.append(current_edu)
        
        return educations
    
    def _extract_skills(self, skills_text: str) -> list[Skill]:
        """Extract skills from text."""
        found_skills = extract_skills(skills_text, self.common_skills)
        
        # Also look for skills mentioned in the text
        skills_list = []
        for skill_name in found_skills:
            skills_list.append(Skill(name=skill_name))
        
        # Extract additional skills from comma-separated lists
        skill_lines = skills_text.split('\n')
        for line in skill_lines:
            if ',' in line and len(line.split(',')) > 2:
                # Likely a skills list
                potential_skills = [s.strip() for s in line.split(',')]
                for ps in potential_skills:
                    if ps and ps not in [s.name for s in skills_list]:
                        skills_list.append(Skill(name=ps))
        
        return skills_list
    
    def _extract_certifications(self, cert_text: str) -> list[Certification]:
        """Extract certifications."""
        certifications = []
        if not cert_text:
            return certifications
        
        lines = cert_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for certification patterns
            if 'Certified' in line or 'Certificate' in line or 'License' in line:
                # Try to extract name and issuer
                parts = line.split(' - ')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    issuer = parts[1].strip()
                else:
                    name = line
                    issuer = "Unknown"
                
                # Look for date
                date_match = re.search(r'(\d{4})', line)
                date = date_match.group(1) if date_match else "Unknown"
                
                certifications.append(Certification(
                    name=name,
                    issuer=issuer,
                    date=date
                ))
        
        return certifications
