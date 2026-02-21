"""Resume data models."""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class ContactInfo(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None


class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    current: bool = False
    description: List[str]
    achievements: Optional[List[str]] = None


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: Optional[List[str]] = None


class Skill(BaseModel):
    name: str
    category: Optional[str] = None  # e.g., "Technical", "Soft", "Language"
    proficiency: Optional[str] = None  # e.g., "Beginner", "Intermediate", "Advanced"


class Certification(BaseModel):
    name: str
    issuer: str
    date: str
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None


class ResumeVersion(BaseModel):
    """Represents a version of a resume."""
    version: int
    created_at: datetime
    changes: Optional[str] = None  # Description of changes
    resume_data: dict  # Snapshot of resume data


class Resume(BaseModel):
    id: str
    filename: str
    uploaded_at: datetime
    contact_info: ContactInfo
    summary: Optional[str] = None
    experience: List[Experience] = []
    education: List[Education] = []
    skills: List[Skill] = []
    certifications: List[Certification] = []
    languages: Optional[List[str]] = None
    projects: Optional[List[dict]] = None
    raw_text: Optional[str] = None
    version: int = 1  # Current version number
    versions: Optional[List[ResumeVersion]] = None  # Version history
    industry: Optional[str] = None  # Industry category
    tags: Optional[List[str]] = None  # Tags for organization
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.versions is None:
            self.versions = []
        if self.tags is None:
            self.tags = []
