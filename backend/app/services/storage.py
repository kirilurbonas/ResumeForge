"""Simple in-memory storage for resumes."""

from typing import Dict, Optional
from app.models.resume_model import Resume


class ResumeStorage:
    """Simple in-memory storage for resumes."""
    
    def __init__(self):
        self.resumes: Dict[str, Resume] = {}
    
    def save(self, resume: Resume) -> Resume:
        """Save a resume."""
        self.resumes[resume.id] = resume
        return resume
    
    def get(self, resume_id: str) -> Optional[Resume]:
        """Get a resume by ID."""
        return self.resumes.get(resume_id)
    
    def delete(self, resume_id: str) -> bool:
        """Delete a resume."""
        if resume_id in self.resumes:
            del self.resumes[resume_id]
            return True
        return False
    
    def list_all(self) -> list[Resume]:
        """List all resumes."""
        return list(self.resumes.values())


# Global storage instance
storage = ResumeStorage()
