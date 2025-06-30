"""
Dependency injection for FastAPI endpoints.
"""

from typing import Optional
from fastapi import HTTPException

from .services.runner_service import RunnerService

# Global runner service instance
_runner_service: Optional[RunnerService] = None


def get_runner_service() -> RunnerService:
    """Get the global runner service instance."""
    if _runner_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return _runner_service


def set_runner_service(service: RunnerService) -> None:
    """Set the global runner service instance."""
    global _runner_service
    _runner_service = service
