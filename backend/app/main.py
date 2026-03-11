"""Main FastAPI application."""

import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ResumeForge",
    description="AI-powered resume analysis and optimization system with FastAPI, ChromaDB, and OpenAI integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api", tags=["authentication"])
app.include_router(router, prefix="/api", tags=["api"])

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database and log startup information."""
    init_db()
    logger.info("ResumeForge API starting up...")
    logger.info("Database initialized")
    logger.info(f"API Documentation available at /docs")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ResumeForge API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }
