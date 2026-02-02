"""API routes for the resume assistant system."""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Form
from fastapi.responses import Response, StreamingResponse
from typing import List, Optional
from pydantic import BaseModel
import os
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
    print(f"Warning: LLM service not initialized: {e}")

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
    job_description: str


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
    
    Supported formats: PDF, DOCX
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")
        
        if not (file.filename.lower().endswith('.pdf') or 
                file.filename.lower().endswith('.docx') or
                file.filename.lower().endswith('.doc')):
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or DOCX.")
        
        # Read file content
        file_content = await file.read()
        
        # Parse resume
        resume = resume_parser.parse(file_content, file.filename)
        
        # Save to storage
        storage.save(resume)
        
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
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
    
    try:
        result = job_matcher.match(resume, request.job_description)
        return result
    except Exception as e:
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
                print(f"Error getting LLM suggestions: {e}")
        
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
        
        return Response(
            content=file_content,
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")
