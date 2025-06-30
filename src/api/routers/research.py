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
from sqlalchemy.orm import Session

from ..models.research import (
    ResearchRequest,
    StartResearchResponse,
    ResearchSession,
    ResearchStatus,
    ProgressUpdate,
    ResearchResult,
    SystemStatus,
    ResearchSessionDB,
    ResearchResultDB,
    ResearchListResponse,
    ResearchUpdateRequest,
    ResearchDeleteResponse,
)
from ..services.runner_service import RunnerService
from ..services.database_service import database_service
from ..database.base import get_db
from ..dependencies import get_runner_service

logger = logging.getLogger(__name__)

router = APIRouter()

# WebSocket connections storage (still in-memory for real-time updates)
websocket_connections: Dict[str, WebSocket] = {}


@router.post("/research/start", response_model=StartResearchResponse)
async def start_research(
    request: ResearchRequest,
    runner_service: RunnerService = Depends(get_runner_service),
    db: Session = Depends(get_db),
):
    """Start a new research session."""

    try:
        # Create session in database
        db_session = database_service.create_research_session(db, request)

        # Start research task asynchronously
        asyncio.create_task(run_research_task(db_session.session_id, request, runner_service))

        return StartResearchResponse(
            session_id=db_session.session_id,
            status=ResearchStatus.PENDING,
            message="Research session started successfully",
        )

    except Exception as e:
        logger.error(f"Error starting research session: {e}")
        raise HTTPException(status_code=500, detail="Failed to start research session")


@router.get("/research/{session_id}/status", response_model=ResearchSessionDB)
async def get_research_status(session_id: str, db: Session = Depends(get_db)):
    """Get the status of a research session."""

    db_session = database_service.get_research_session(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    return ResearchSessionDB.model_validate(db_session)


@router.get("/research/{session_id}/result", response_model=List[ResearchResultDB])
async def get_research_result(session_id: str, db: Session = Depends(get_db)):
    """Get the results of a research session."""

    # Check if session exists
    db_session = database_service.get_research_session(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get all results for this session
    results = database_service.get_research_results_by_session(db, session_id)

    return [ResearchResultDB.model_validate(result) for result in results]


@router.get("/research/sessions", response_model=List[ResearchSessionDB])
async def list_research_sessions(
    page: int = 1,
    page_size: int = 20,
    status_filter: ResearchStatus = None,
    db: Session = Depends(get_db),
):
    """List research sessions with pagination."""

    sessions, total_count = database_service.list_research_sessions(
        db, page=page, page_size=page_size, status_filter=status_filter
    )

    return [ResearchSessionDB.model_validate(session) for session in sessions]


@router.delete("/research/{session_id}")
async def delete_research_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a research session and its results."""

    # Check if session exists
    db_session = database_service.get_research_session(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Close WebSocket connection if exists
    if session_id in websocket_connections:
        try:
            await websocket_connections[session_id].close()
        except:
            pass
        del websocket_connections[session_id]

    # Delete all results for this session (handled by cascade delete in SQLAlchemy)
    # Then delete the session
    try:
        db.delete(db_session)
        db.commit()
        return {"message": "Session deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete session")


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
        # Send initial status if session exists in database
        from ..database.base import SessionLocal

        db = SessionLocal()
        try:
            db_session = database_service.get_research_session(db, session_id)
            if db_session:
                update = ProgressUpdate(
                    session_id=session_id,
                    status=db_session.status,
                    progress_percentage=db_session.progress_percentage,
                    current_step=db_session.current_step,
                )
                await websocket.send_json(update.model_dump())
        finally:
            db.close()

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
        if request.output_format.value == "blog_post":
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

        elif request.output_format.value == "book_chapter":
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

        elif request.output_format.value == "research_report":
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

        elif request.output_format.value == "interactive_session":
            result = await runner_service.create_interactive_session(
                topic=request.topic,
                content_directions=request.content_directions,
                target_audience=request.target_audience.value,
                progress_callback=lambda status, progress, step: asyncio.create_task(
                    update_session_progress(session_id, status, progress, step)
                ),
            )

        # Save result to database and update session status
        from ..database.base import SessionLocal

        db = SessionLocal()
        try:
            # Save research result to database
            result.session_id = session_id  # Make sure session_id is set
            db_result = database_service.create_research_result(
                db,
                session_id=session_id,
                title=result.title,
                content=result.content,
                sources=result.sources,
                agent_contributions=result.agent_contributions,
                output_format=result.output_format,
                summary=result.summary,
                key_concepts=result.key_concepts,
                exercises=result.exercises,
                learning_objectives=result.learning_objectives,
            )

            # Update session status to completed
            database_service.update_research_session_status(
                db, session_id, ResearchStatus.COMPLETED, 100, "Research completed successfully"
            )

            # Send final update via WebSocket
            await send_websocket_update(
                session_id, db, ResearchStatus.COMPLETED, 100, "Research completed successfully"
            )

        except Exception as e:
            logger.error(f"Error saving research result for session {session_id}: {e}")
            # Update session with error
            database_service.update_research_session_status(
                db, session_id, ResearchStatus.FAILED, 0, "Failed to save research result", str(e)
            )
        finally:
            db.close()

    except Exception as e:
        logger.error(f"Research task failed for session {session_id}: {e}")

        # Update session with error in database
        from ..database.base import SessionLocal

        db = SessionLocal()
        try:
            database_service.update_research_session_status(
                db, session_id, ResearchStatus.FAILED, 0, "Research task failed", str(e)
            )

            # Send error update via WebSocket
            await send_websocket_update(
                session_id, db, ResearchStatus.FAILED, 0, "Research task failed"
            )
        finally:
            db.close()


async def update_session_progress(
    session_id: str, status: ResearchStatus, progress: int, step: str
):
    """Update session progress and notify WebSocket clients."""

    from ..database.base import SessionLocal

    db = SessionLocal()
    try:
        # Update session in database
        database_service.update_research_session_status(db, session_id, status, progress, step)

        # Send update via WebSocket
        await send_websocket_update(session_id, db, status, progress, step)
    finally:
        db.close()


async def send_websocket_update(
    session_id: str, db: Session, status: ResearchStatus, progress: int, step: str
):
    """Send progress update via WebSocket."""

    if session_id not in websocket_connections:
        return

    websocket = websocket_connections[session_id]

    try:
        update = ProgressUpdate(
            session_id=session_id,
            status=status,
            progress_percentage=progress,
            current_step=step,
        )
        await websocket.send_json(update.model_dump())
    except:
        # Connection might be closed, remove it
        if session_id in websocket_connections:
            del websocket_connections[session_id]


# Research Results Management Endpoints

@router.get("/research/results", response_model=ResearchListResponse)
async def list_research_results(
    page: int = 1,
    page_size: int = 20,
    search_query: str = None,
    output_format: str = None,
    db: Session = Depends(get_db),
):
    """List research results with pagination and filtering."""
    
    try:
        # Convert string output_format to enum if provided
        format_filter = None
        if output_format:
            try:
                from ..models.research import OutputFormat
                format_filter = OutputFormat(output_format)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid output format: {output_format}")
        
        results, total_count = database_service.list_research_results(
            db, 
            page=page, 
            page_size=page_size, 
            search_query=search_query,
            output_format=format_filter
        )
        
        return ResearchListResponse(
            total=total_count,
            page=page,
            page_size=page_size,
            items=[ResearchResultDB.model_validate(result) for result in results]
        )
    
    except Exception as e:
        logger.error(f"Error listing research results: {e}")
        raise HTTPException(status_code=500, detail="Failed to list research results")


@router.get("/research/results/{result_id}", response_model=ResearchResultDB)
async def get_research_result_by_id(result_id: str, db: Session = Depends(get_db)):
    """Get a specific research result by ID."""
    
    result = database_service.get_research_result(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Research result not found")
    
    return ResearchResultDB.model_validate(result)


@router.put("/research/results/{result_id}", response_model=ResearchResultDB)
async def update_research_result(
    result_id: str, 
    update_data: ResearchUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update a research result."""
    
    try:
        updated_result = database_service.update_research_result(db, result_id, update_data)
        if not updated_result:
            raise HTTPException(status_code=404, detail="Research result not found")
        
        return ResearchResultDB.model_validate(updated_result)
    
    except Exception as e:
        logger.error(f"Error updating research result {result_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update research result")


@router.delete("/research/results/{result_id}", response_model=ResearchDeleteResponse)
async def delete_research_result(result_id: str, db: Session = Depends(get_db)):
    """Delete a research result."""
    
    try:
        success = database_service.delete_research_result(db, result_id)
        if not success:
            raise HTTPException(status_code=404, detail="Research result not found")
        
        return ResearchDeleteResponse(
            success=True,
            message="Research result deleted successfully",
            deleted_result_id=result_id
        )
    
    except Exception as e:
        logger.error(f"Error deleting research result {result_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete research result")
