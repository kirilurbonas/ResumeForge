"""Database-backed storage for resumes."""

from typing import Dict, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
import json
import uuid

from app.models.resume_model import Resume, ResumeVersion
from app.database import ResumeDB, ResumeVersionDB


class DatabaseStorage:
    """Database-backed storage for resumes."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, resume: Resume, user_id: str, create_version: bool = False, change_description: Optional[str] = None) -> Resume:
        """Save a resume to database."""
        # Check if resume exists
        db_resume = self.db.query(ResumeDB).filter(ResumeDB.id == resume.id).first()
        
        if db_resume:
            # Update existing resume
            if create_version:
                # Create version snapshot
                version = ResumeVersionDB(
                    id=str(uuid.uuid4()),
                    resume_id=resume.id,
                    version=resume.version,
                    created_at=datetime.utcnow(),
                    changes=change_description,
                    resume_data=json.loads(resume.json())
                )
                self.db.add(version)
                resume.version = resume.version + 1
            
            # Update resume data
            db_resume.resume_data = json.loads(resume.json())
            db_resume.version = resume.version
            db_resume.industry = resume.industry
            db_resume.tags = resume.tags if resume.tags else []
        else:
            # Create new resume
            db_resume = ResumeDB(
                id=resume.id,
                user_id=user_id,
                filename=resume.filename,
                uploaded_at=resume.uploaded_at,
                resume_data=json.loads(resume.json()),
                version=resume.version,
                industry=resume.industry,
                tags=resume.tags if resume.tags else []
            )
            self.db.add(db_resume)
        
        self.db.commit()
        self.db.refresh(db_resume)
        
        # Reload resume from database
        return self._db_to_resume(db_resume)
    
    def get(self, resume_id: str, user_id: Optional[str] = None) -> Optional[Resume]:
        """Get a resume by ID."""
        query = self.db.query(ResumeDB).filter(ResumeDB.id == resume_id)
        if user_id:
            query = query.filter(ResumeDB.user_id == user_id)
        
        db_resume = query.first()
        if not db_resume:
            return None
        
        return self._db_to_resume(db_resume)
    
    def get_version(self, resume_id: str, version: int, user_id: Optional[str] = None) -> Optional[Resume]:
        """Get a specific version of a resume."""
        # Check if it's current version
        resume = self.get(resume_id, user_id)
        if resume and resume.version == version:
            return resume
        
        # Check version history
        query = self.db.query(ResumeVersionDB).filter(
            ResumeVersionDB.resume_id == resume_id,
            ResumeVersionDB.version == version
        )
        
        db_version = query.first()
        if not db_version:
            return None
        
        # Reconstruct resume from version data
        resume_data = db_version.resume_data
        return Resume(**resume_data)
    
    def list_versions(self, resume_id: str, user_id: Optional[str] = None) -> List[ResumeVersion]:
        """List all versions of a resume."""
        # Get current resume
        resume = self.get(resume_id, user_id)
        if not resume:
            return []
        
        # Get version history
        query = self.db.query(ResumeVersionDB).filter(ResumeVersionDB.resume_id == resume_id)
        db_versions = query.order_by(ResumeVersionDB.version).all()
        
        versions = []
        for db_v in db_versions:
            versions.append(ResumeVersion(
                version=db_v.version,
                created_at=db_v.created_at,
                changes=db_v.changes,
                resume_data=db_v.resume_data
            ))
        
        # Add current version
        versions.append(ResumeVersion(
            version=resume.version,
            created_at=datetime.utcnow(),
            changes="Current version",
            resume_data=json.loads(resume.json())
        ))
        
        return versions
    
    def create_version(self, resume_id: str, user_id: str, change_description: Optional[str] = None) -> Optional[Resume]:
        """Create a new version of an existing resume."""
        resume = self.get(resume_id, user_id)
        if not resume:
            return None
        
        return self.save(resume, user_id, create_version=True, change_description=change_description)
    
    def delete(self, resume_id: str, user_id: Optional[str] = None) -> bool:
        """Delete a resume."""
        query = self.db.query(ResumeDB).filter(ResumeDB.id == resume_id)
        if user_id:
            query = query.filter(ResumeDB.user_id == user_id)
        
        db_resume = query.first()
        if not db_resume:
            return False
        
        # Delete versions
        self.db.query(ResumeVersionDB).filter(ResumeVersionDB.resume_id == resume_id).delete()
        
        # Delete resume
        self.db.delete(db_resume)
        self.db.commit()
        return True
    
    def list_all(self, user_id: Optional[str] = None) -> List[Resume]:
        """List all resumes."""
        query = self.db.query(ResumeDB)
        if user_id:
            query = query.filter(ResumeDB.user_id == user_id)
        
        db_resumes = query.all()
        return [self._db_to_resume(db_r) for db_r in db_resumes]
    
    def list_by_industry(self, industry: str, user_id: Optional[str] = None) -> List[Resume]:
        """List resumes filtered by industry."""
        query = self.db.query(ResumeDB).filter(ResumeDB.industry == industry)
        if user_id:
            query = query.filter(ResumeDB.user_id == user_id)
        
        db_resumes = query.all()
        return [self._db_to_resume(db_r) for db_r in db_resumes]
    
    def list_by_tag(self, tag: str, user_id: Optional[str] = None) -> List[Resume]:
        """List resumes filtered by tag."""
        query = self.db.query(ResumeDB)
        if user_id:
            query = query.filter(ResumeDB.user_id == user_id)
        
        db_resumes = query.all()
        return [r for r in [self._db_to_resume(db_r) for db_r in db_resumes] if tag in (r.tags or [])]
    
    def _db_to_resume(self, db_resume: ResumeDB) -> Resume:
        """Convert database model to Resume."""
        resume_data = db_resume.resume_data
        resume_data['id'] = db_resume.id
        resume_data['filename'] = db_resume.filename
        resume_data['uploaded_at'] = db_resume.uploaded_at.isoformat() if isinstance(db_resume.uploaded_at, datetime) else db_resume.uploaded_at
        resume_data['version'] = db_resume.version
        resume_data['industry'] = db_resume.industry
        resume_data['tags'] = db_resume.tags or []
        
        return Resume(**resume_data)
