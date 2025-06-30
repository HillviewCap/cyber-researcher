"""
Research API endpoints.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import FileResponse

from ..models.research import (
    ResearchRequest,
    StartResearchResponse,
    ResearchSession,
    ResearchStatus,
    ProgressUpdate,
    ResearchResult,
    SystemStatus,
)
from ..services.runner_service import RunnerService
from ..dependencies import get_runner_service

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory session storage (in production, use Redis or database)
active_sessions: Dict[str, ResearchSession] = {}
websocket_connections: Dict[str, WebSocket] = {}


@router.post("/research/start", response_model=StartResearchResponse)
async def start_research(
    request: ResearchRequest, runner_service: RunnerService = Depends(get_runner_service)
):
    """Start a new research session."""

    # Generate session ID
    session_id = str(uuid4())

    # Create session
    session = ResearchSession(
        session_id=session_id,
        request=request,
        status=ResearchStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # Store session
    active_sessions[session_id] = session

    # Start research task asynchronously
    asyncio.create_task(run_research_task(session_id, request, runner_service))

    return StartResearchResponse(
        session_id=session_id,
        status=ResearchStatus.PENDING,
        message="Research session started successfully",
    )


@router.get("/research/{session_id}/status", response_model=ResearchSession)
async def get_research_status(session_id: str):
    """Get the status of a research session."""

    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return active_sessions[session_id]


@router.get("/research/{session_id}/result", response_model=ResearchResult)
async def get_research_result(session_id: str):
    """Get the result of a completed research session."""

    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = active_sessions[session_id]

    if session.status != ResearchStatus.COMPLETED:
        raise HTTPException(
            status_code=400, detail=f"Research not completed. Current status: {session.status}"
        )

    if session.result is None:
        raise HTTPException(status_code=500, detail="Result not available")

    return session.result


@router.get("/research/sessions", response_model=List[ResearchSession])
async def list_research_sessions():
    """List all research sessions."""
    return list(active_sessions.values())


@router.delete("/research/{session_id}")
async def delete_research_session(session_id: str):
    """Delete a research session."""

    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    # Close WebSocket connection if exists
    if session_id in websocket_connections:
        try:
            await websocket_connections[session_id].close()
        except:
            pass
        del websocket_connections[session_id]

    # Remove session
    del active_sessions[session_id]

    return {"message": "Session deleted successfully"}


@router.get("/config", response_model=SystemStatus)
async def get_system_config(runner_service: RunnerService = Depends(get_runner_service)):
    """Get system configuration and status."""

    status = await runner_service.get_system_status()
    return SystemStatus(**status)


@router.websocket("/ws/research/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time progress updates."""

    await websocket.accept()
    websocket_connections[session_id] = websocket

    try:
        # Send initial status if session exists
        if session_id in active_sessions:
            session = active_sessions[session_id]
            update = ProgressUpdate(
                session_id=session_id,
                status=session.status,
                progress_percentage=session.progress_percentage,
                current_step=session.current_step,
            )
            await websocket.send_json(update.dict())

        # Keep connection alive and listen for client messages
        while True:
            try:
                data = await websocket.receive_text()
                # Handle any client messages if needed
            except WebSocketDisconnect:
                break

    except WebSocketDisconnect:
        pass
    finally:
        # Clean up connection
        if session_id in websocket_connections:
            del websocket_connections[session_id]


async def run_research_task(
    session_id: str, request: ResearchRequest, runner_service: RunnerService
):
    """Run the research task asynchronously."""

    try:
        # Update session status
        await update_session_progress(
            session_id, ResearchStatus.INITIALIZING, 10, "Initializing research agents..."
        )

        # Perform research based on output format
        if request.output_format == "blog_post":
            result = await runner_service.generate_blog_post(
                topic=request.topic,
                content_directions=request.content_directions,
                style=request.style,
                target_audience=request.target_audience.value,
                technical_depth=request.technical_depth.value,
                include_historical_context=request.include_historical_context,
                progress_callback=lambda status, progress, step: asyncio.create_task(
                    update_session_progress(session_id, status, progress, step)
                ),
            )

        elif request.output_format == "book_chapter":
            result = await runner_service.generate_book_chapter(
                topic=request.topic,
                content_directions=request.content_directions,
                chapter_number=request.chapter_number or 1,
                learning_objectives=request.learning_objectives or [],
                target_audience=request.target_audience.value,
                technical_depth=request.technical_depth.value,
                include_historical_context=request.include_historical_context,
                progress_callback=lambda status, progress, step: asyncio.create_task(
                    update_session_progress(session_id, status, progress, step)
                ),
            )

        elif request.output_format == "research_report":
            result = await runner_service.generate_research_report(
                topic=request.topic,
                content_directions=request.content_directions,
                report_type=request.report_type or "threat_assessment",
                confidentiality=request.confidentiality or "internal",
                target_audience=request.target_audience.value,
                technical_depth=request.technical_depth.value,
                include_historical_context=request.include_historical_context,
                progress_callback=lambda status, progress, step: asyncio.create_task(
                    update_session_progress(session_id, status, progress, step)
                ),
            )

        elif request.output_format == "interactive_session":
            result = await runner_service.create_interactive_session(
                topic=request.topic,
                content_directions=request.content_directions,
                target_audience=request.target_audience.value,
                progress_callback=lambda status, progress, step: asyncio.create_task(
                    update_session_progress(session_id, status, progress, step)
                ),
            )

        # Update session with result
        if session_id in active_sessions:
            session = active_sessions[session_id]
            session.result = result
            session.status = ResearchStatus.COMPLETED
            session.progress_percentage = 100
            session.current_step = "Research completed successfully"
            session.updated_at = datetime.now()

            # Send final update via WebSocket
            await send_websocket_update(session_id, session)

    except Exception as e:
        logger.error(f"Research task failed for session {session_id}: {e}")

        # Update session with error
        if session_id in active_sessions:
            session = active_sessions[session_id]
            session.status = ResearchStatus.FAILED
            session.error_message = str(e)
            session.updated_at = datetime.now()

            # Send error update via WebSocket
            await send_websocket_update(session_id, session)


async def update_session_progress(
    session_id: str, status: ResearchStatus, progress: int, step: str
):
    """Update session progress and notify WebSocket clients."""

    if session_id not in active_sessions:
        return

    session = active_sessions[session_id]
    session.status = status
    session.progress_percentage = progress
    session.current_step = step
    session.updated_at = datetime.now()

    # Send update via WebSocket
    await send_websocket_update(session_id, session)


async def send_websocket_update(session_id: str, session: ResearchSession):
    """Send progress update via WebSocket."""

    if session_id not in websocket_connections:
        return

    websocket = websocket_connections[session_id]

    try:
        update = ProgressUpdate(
            session_id=session_id,
            status=session.status,
            progress_percentage=session.progress_percentage,
            current_step=session.current_step,
        )
        await websocket.send_json(update.dict())
    except:
        # Connection might be closed, remove it
        if session_id in websocket_connections:
            del websocket_connections[session_id]
