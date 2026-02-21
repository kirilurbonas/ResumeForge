"""API routes for the resume assistant system."""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Form
from fastapi.responses import Response, StreamingResponse
from typing import List, Optional
from pydantic import BaseModel, Field
import os
import logging
from datetime import datetime

from app.services.resume_parser import ResumeParser
from app.services.resume_analyzer import ResumeAnalyzer
from app.services.ats_optimizer import ATSOptimizer
from app.services.skills_analyzer import SkillsAnalyzer
from app.services.job_matcher import JobMatcher
from app.services.format_optimizer import FormatOptimizer
from app.services.resume_generator import ResumeGenerator
from app.services.template_engine import TemplateEngine
from app.services.storage import storage
from app.services.llm_service import initialize_llm_service, llm_service

# Configure logging
logger = logging.getLogger(__name__)

# Constants
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB default
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc'}

# Initialize services
resume_parser = ResumeParser()
resume_analyzer = ResumeAnalyzer()
ats_optimizer = ATSOptimizer()
skills_analyzer = SkillsAnalyzer()
job_matcher = JobMatcher()
format_optimizer = FormatOptimizer()
resume_generator = ResumeGenerator()
template_engine = TemplateEngine()

# Initialize LLM service
try:
    initialize_llm_service()
except Exception as e:
    logger.warning(f"LLM service not initialized: {e}")

router = APIRouter()


# Request/Response models
class ResumeResponse(BaseModel):
    id: str
    filename: str
    uploaded_at: str
    contact_info: dict
    summary: Optional[str] = None
    experience_count: int
    education_count: int
    skills_count: int


class AnalysisResponse(BaseModel):
    resume_id: str
    ats_score: int
    strengths: List[str]
    weaknesses: List[str]
    metrics: dict
    keyword_analysis: dict


class ATSOptimizeRequest(BaseModel):
    job_description: Optional[str] = None


class JobMatchRequest(BaseModel):
    job_description: str = Field(..., min_length=10, description="Job description text (minimum 10 characters)")


class TemplateResponse(BaseModel):
    id: str
    name: str
    description: str
    ats_friendly: bool
    preview_url: Optional[str] = None


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "resume-forge"}


@router.post("/resume/upload", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume.
    
    Supported formats: PDF, DOCX, DOC
    Maximum file size: 10MB (configurable via MAX_FILE_SIZE env var)
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")
        
        # Check file extension
        file_ext = os.path.splitext(file.filename.lower())[1]
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Supported formats: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size
        file_size = len(file_content)
        if file_size > MAX_FILE_SIZE:
            max_size_mb = MAX_FILE_SIZE / (1024 * 1024)
            raise HTTPException(
                status_code=400,
                detail=f"File size ({file_size / (1024 * 1024):.2f}MB) exceeds maximum allowed size ({max_size_mb}MB)"
            )
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        logger.info(f"Processing resume upload: {file.filename} ({file_size} bytes)")
        
        # Parse resume
        resume = resume_parser.parse(file_content, file.filename)
        
        # Save to storage
        storage.save(resume)
        
        logger.info(f"Successfully parsed and saved resume: {resume.id}")
        
        return ResumeResponse(
            id=resume.id,
            filename=resume.filename,
            uploaded_at=resume.uploaded_at.isoformat(),
            contact_info=resume.contact_info.dict(),
            summary=resume.summary,
            experience_count=len(resume.experience),
            education_count=len(resume.education),
            skills_count=len(resume.skills)
        )
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error during resume upload: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing resume: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


@router.get("/resume/{resume_id}")
async def get_resume(resume_id: str):
    """Get parsed resume data."""
    resume = storage.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return {
        "id": resume.id,
        "filename": resume.filename,
        "uploaded_at": resume.uploaded_at.isoformat(),
        "contact_info": resume.contact_info.dict(),
        "summary": resume.summary,
        "experience": [exp.dict() for exp in resume.experience],
        "education": [edu.dict() for edu in resume.education],
        "skills": [skill.dict() for skill in resume.skills],
        "certifications": [cert.dict() for cert in resume.certifications]
    }


@router.post("/resume/{resume_id}/analyze", response_model=AnalysisResponse)
async def analyze_resume(resume_id: str):
    """Run full analysis on resume."""
    resume = storage.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    try:
        analysis = resume_analyzer.analyze(resume)
        
        return AnalysisResponse(
            resume_id=resume_id,
            ats_score=analysis['ats_score'],
            strengths=analysis['strengths'],
            weaknesses=analysis['weaknesses'],
            metrics=analysis['metrics'],
            keyword_analysis=analysis['keyword_analysis']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@router.post("/resume/{resume_id}/ats-optimize")
async def optimize_ats(resume_id: str, request: ATSOptimizeRequest):
    """Get ATS optimization suggestions."""
    resume = storage.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    try:
        result = ats_optimizer.optimize(resume, request.job_description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing resume: {str(e)}")


@router.post("/resume/{resume_id}/match-job")
async def match_job(resume_id: str, request: JobMatchRequest):
    """Match resume to job description."""
    resume = storage.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Validate job description
    if not request.job_description or len(request.job_description.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Job description must be at least 10 characters long"
        )
    
    try:
        logger.info(f"Matching resume {resume_id} to job description")
        result = job_matcher.match(resume, request.job_description)
        return result
    except Exception as e:
        logger.error(f"Error matching resume: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error matching resume: {str(e)}")


@router.get("/resume/{resume_id}/suggestions")
async def get_suggestions(resume_id: str):
    """Get improvement suggestions."""
    resume = storage.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    try:
        # Run analysis first
        analysis = resume_analyzer.analyze(resume)
        
        # Get LLM suggestions if available
        suggestions = []
        if llm_service:
            try:
                llm_suggestions = await llm_service.generate_suggestions(
                    resume.raw_text or "",
                    analysis
                )
                suggestions.append(llm_suggestions)
            except Exception as e:
                logger.warning(f"Error getting LLM suggestions: {e}")
        
        # Add format optimizer suggestions
        format_suggestions = format_optimizer.get_formatting_suggestions(resume)
        suggestions.extend(format_suggestions)
        
        return {
            "resume_id": resume_id,
            "suggestions": suggestions,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting suggestions: {str(e)}")


@router.delete("/resume/{resume_id}")
async def delete_resume(resume_id: str):
    """Delete a resume."""
    success = storage.delete(resume_id)
    if not success:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Resume deleted successfully"}


@router.get("/templates", response_model=List[TemplateResponse])
async def list_templates():
    """List available resume templates."""
    templates = template_engine.list_templates()
    return [
        TemplateResponse(
            id=t['id'],
            name=t['name'],
            description=t['description'],
            ats_friendly=t.get('ats_friendly', True)
        )
        for t in templates
    ]


@router.get("/templates/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: str):
    """Get template details."""
    template = template_engine.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return TemplateResponse(
        id=template['id'],
        name=template['name'],
        description=template['description'],
        ats_friendly=template.get('ats_friendly', True)
    )


@router.post("/resume/{resume_id}/improve-format")
async def improve_format(resume_id: str):
    """Apply format improvements to resume."""
    resume = storage.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    try:
        result = format_optimizer.optimize(resume)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error improving format: {str(e)}")


@router.post("/resume/{resume_id}/generate")
async def generate_resume(
    resume_id: str,
    template_id: str = Query(..., description="Template ID to use"),
    format: str = Query("doc", description="Output format: doc or pdf")
):
    """Generate resume in selected template and format."""
    resume = storage.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Validate template
    if not template_engine.template_exists(template_id):
        raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
    
    # Validate format
    if format not in ['doc', 'pdf']:
        raise HTTPException(status_code=400, detail="Format must be 'doc' or 'pdf'")
    
    try:
        # Generate resume
        if format == 'doc':
            file_content = resume_generator.generate_doc(resume, template_id)
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"{resume.contact_info.name.replace(' ', '_')}_resume.docx"
        else:  # pdf
            file_content = resume_generator.generate_pdf(resume, template_id)
            media_type = "application/pdf"
            filename = f"{resume.contact_info.name.replace(' ', '_')}_resume.pdf"
        
        logger.info(f"Generated {format.upper()} resume for {resume_id} using template {template_id}")
        
        return Response(
            content=file_content,
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating resume: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")
