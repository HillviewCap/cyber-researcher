"""
FastAPI main application for Cyber-Researcher frontend.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routers import research
from .services.runner_service import RunnerService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global runner service instance
runner_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global runner_service
    
    # Startup
    logger.info("Initializing Cyber-Researcher API...")
    try:
        runner_service = RunnerService()
        await runner_service.initialize()
        logger.info("✓ Cyber-Researcher API initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize API: {e}")
        # Continue with limited functionality
    
    yield
    
    # Shutdown
    logger.info("Shutting down Cyber-Researcher API...")


# Create FastAPI app
app = FastAPI(
    title="Cyber-Researcher API",
    description="Backend API for the Cyber-Researcher frontend interface",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research.router, prefix="/api", tags=["research"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Cyber-Researcher API", "version": "1.0.0"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    if runner_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    status = await runner_service.get_system_status()
    return {"status": "healthy", "system": status}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


def get_runner_service() -> RunnerService:
    """Get the global runner service instance."""
    if runner_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return runner_service