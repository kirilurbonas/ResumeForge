"""Simple in-memory storage for resumes."""

from typing import Dict, Optional, List
from datetime import datetime
from app.models.resume_model import Resume, ResumeVersion
import copy


class ResumeStorage:
    """Simple in-memory storage for resumes with version management."""
    
    def __init__(self):
        self.resumes: Dict[str, Resume] = {}
        self.resume_groups: Dict[str, List[str]] = {}  # Group resumes by base ID
    
    def save(self, resume: Resume, create_version: bool = False, change_description: Optional[str] = None) -> Resume:
        """
        Save a resume, optionally creating a version snapshot.
        
        Args:
            resume: Resume to save
            create_version: Whether to create a version snapshot
            change_description: Description of changes made
        """
        # If creating a version, save current state
        if create_version and resume.id in self.resumes:
            existing = self.resumes[resume.id]
            resume.version = existing.version + 1
            
            # Create version snapshot
            version = ResumeVersion(
                version=existing.version,
                created_at=datetime.now(),
                changes=change_description,
                resume_data=existing.dict()
            )
            resume.versions = existing.versions + [version]
        
        self.resumes[resume.id] = resume
        return resume
    
    def get(self, resume_id: str) -> Optional[Resume]:
        """Get a resume by ID."""
        return self.resumes.get(resume_id)
    
    def get_version(self, resume_id: str, version: int) -> Optional[Resume]:
        """Get a specific version of a resume."""
        resume = self.get(resume_id)
        if not resume:
            return None
        
        # Find version in history
        for v in resume.versions:
            if v.version == version:
                # Reconstruct resume from version data
                return Resume(**v.resume_data)
        
        # If version is current version
        if resume.version == version:
            return resume
        
        return None
    
    def list_versions(self, resume_id: str) -> List[ResumeVersion]:
        """List all versions of a resume."""
        resume = self.get(resume_id)
        if not resume:
            return []
        return resume.versions + [ResumeVersion(
            version=resume.version,
            created_at=datetime.now(),
            changes="Current version",
            resume_data=resume.dict()
        )]
    
    def create_version(self, resume_id: str, change_description: Optional[str] = None) -> Optional[Resume]:
        """Create a new version of an existing resume."""
        resume = self.get(resume_id)
        if not resume:
            return None
        
        # Create a copy with new ID for versioning
        new_resume = copy.deepcopy(resume)
        new_resume.version = resume.version + 1
        
        # Add current resume as version
        version = ResumeVersion(
            version=resume.version,
            created_at=datetime.now(),
            changes=change_description or "Version snapshot",
            resume_data=resume.dict()
        )
        new_resume.versions = resume.versions + [version]
        
        self.resumes[resume_id] = new_resume
        return new_resume
    
    def delete(self, resume_id: str) -> bool:
        """Delete a resume."""
        if resume_id in self.resumes:
            del self.resumes[resume_id]
            return True
        return False
    
    def list_all(self) -> List[Resume]:
        """List all resumes."""
        return list(self.resumes.values())
    
    def list_by_industry(self, industry: str) -> List[Resume]:
        """List resumes filtered by industry."""
        return [r for r in self.resumes.values() if r.industry == industry]
    
    def list_by_tag(self, tag: str) -> List[Resume]:
        """List resumes filtered by tag."""
        return [r for r in self.resumes.values() if tag in (r.tags or [])]


# Global storage instance
storage = ResumeStorage()
