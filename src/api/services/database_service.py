"""
Database service layer for research operations.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import uuid4

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc, and_, or_

from ..database.models import ResearchSession, ResearchResult, ResearchMetadata, AgentActivity
from ..database.base import get_db
from ..models.research import (
    ResearchRequest,
    ResearchStatus,
    OutputFormat,
    TargetAudience,
    TechnicalDepth,
    ResearchSessionDB,
    ResearchResultDB,
    ResearchUpdateRequest,
)

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service layer for database operations."""

    def __init__(self):
        """Initialize the database service."""
        pass

    def create_research_session(self, db: Session, request: ResearchRequest) -> ResearchSession:
        """
        Create a new research session in the database.

        Args:
            db: Database session
            request: Research request data

        Returns:
            Created research session
        """
        try:
            session_id = str(uuid4())

            from ..database.models import (
                OutputFormatEnum,
                TargetAudienceEnum,
                TechnicalDepthEnum,
                ResearchStatusEnum,
            )

            db_session = ResearchSession(
                session_id=session_id,
                topic=request.topic,
                content_directions=request.content_directions,
                output_format=OutputFormatEnum(request.output_format.value),
                target_audience=TargetAudienceEnum(request.target_audience.value),
                technical_depth=TechnicalDepthEnum(request.technical_depth.value),
                include_historical_context=request.include_historical_context,
                style=request.style,
                chapter_number=request.chapter_number,
                learning_objectives=request.learning_objectives,
                report_type=request.report_type,
                confidentiality=request.confidentiality,
                status=ResearchStatusEnum.PENDING,
                progress_percentage=0,
                current_step="initializing",
            )

            db.add(db_session)
            db.commit()
            db.refresh(db_session)

            logger.info(f"Created research session: {session_id}")
            return db_session

        except SQLAlchemyError as e:
            logger.error(f"Database error creating research session: {e}")
            db.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating research session: {e}")
            db.rollback()
            raise

    def get_research_session(self, db: Session, session_id: str) -> Optional[ResearchSession]:
        """
        Get a research session by ID.

        Args:
            db: Database session
            session_id: Session ID to retrieve

        Returns:
            Research session or None if not found
        """
        try:
            return (
                db.query(ResearchSession).filter(ResearchSession.session_id == session_id).first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving research session {session_id}: {e}")
            raise

    def update_research_session_status(
        self,
        db: Session,
        session_id: str,
        status: ResearchStatus,
        progress_percentage: int,
        current_step: str,
        error_message: Optional[str] = None,
    ) -> Optional[ResearchSession]:
        """
        Update research session status and progress.

        Args:
            db: Database session
            session_id: Session ID to update
            status: New status
            progress_percentage: Progress percentage (0-100)
            current_step: Current step description
            error_message: Error message if status is FAILED

        Returns:
            Updated research session or None if not found
        """
        try:
            db_session = (
                db.query(ResearchSession).filter(ResearchSession.session_id == session_id).first()
            )

            if not db_session:
                return None

            from ..database.models import ResearchStatusEnum

            db_session.status = (
                ResearchStatusEnum(status.value)
                if hasattr(status, "value")
                else ResearchStatusEnum(status)
            )
            db_session.progress_percentage = progress_percentage
            db_session.current_step = current_step
            db_session.error_message = error_message
            db_session.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(db_session)

            logger.info(f"Updated session {session_id} status to {status}")
            return db_session

        except SQLAlchemyError as e:
            logger.error(f"Database error updating research session {session_id}: {e}")
            db.rollback()
            raise

    def create_research_result(
        self,
        db: Session,
        session_id: str,
        title: str,
        content: str,
        sources: List[str],
        agent_contributions: Dict[str, Dict[str, Any]],
        output_format: OutputFormat,
        metadata: Optional[Dict[str, Any]] = None,
        summary: Optional[str] = None,
        key_concepts: Optional[List[str]] = None,
        exercises: Optional[List[str]] = None,
        learning_objectives: Optional[List[str]] = None,
    ) -> ResearchResult:
        """
        Create a research result in the database.

        Args:
            db: Database session
            session_id: Associated session ID
            title: Result title
            content: Result content
            sources: List of sources
            agent_contributions: Agent contribution data
            output_format: Output format
            metadata: Optional technical metadata
            summary: Optional summary
            key_concepts: Optional key concepts
            exercises: Optional exercises
            learning_objectives: Optional learning objectives

        Returns:
            Created research result
        """
        try:
            result_id = str(uuid4())

            from ..database.models import OutputFormatEnum

            db_result = ResearchResult(
                result_id=result_id,
                session_id=session_id,
                title=title,
                content=content,
                sources=sources,
                agent_contributions=agent_contributions,
                technical_metadata=metadata or {},
                output_format=(
                    OutputFormatEnum(output_format.value)
                    if hasattr(output_format, "value")
                    else OutputFormatEnum(output_format)
                ),
                summary=summary,
                key_concepts=key_concepts,
                exercises=exercises,
                learning_objectives=learning_objectives,
            )

            db.add(db_result)
            db.commit()
            db.refresh(db_result)

            logger.info(f"Created research result: {result_id}")
            return db_result

        except SQLAlchemyError as e:
            logger.error(f"Database error creating research result: {e}")
            db.rollback()
            raise

    def get_research_result(self, db: Session, result_id: str) -> Optional[ResearchResult]:
        """
        Get a research result by ID.

        Args:
            db: Database session
            result_id: Result ID to retrieve

        Returns:
            Research result or None if not found
        """
        try:
            return db.query(ResearchResult).filter(ResearchResult.result_id == result_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving research result {result_id}: {e}")
            raise

    def get_research_results_by_session(self, db: Session, session_id: str) -> List[ResearchResult]:
        """
        Get all research results for a session.

        Args:
            db: Database session
            session_id: Session ID

        Returns:
            List of research results
        """
        try:
            return (
                db.query(ResearchResult)
                .filter(ResearchResult.session_id == session_id)
                .order_by(desc(ResearchResult.created_at))
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving results for session {session_id}: {e}")
            raise

    def list_research_results(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        search_query: Optional[str] = None,
        output_format: Optional[OutputFormat] = None,
    ) -> tuple[List[ResearchResult], int]:
        """
        List research results with pagination and filtering.

        Args:
            db: Database session
            page: Page number (1-based)
            page_size: Number of items per page
            search_query: Optional search query for title/content
            output_format: Optional output format filter

        Returns:
            Tuple of (results, total_count)
        """
        try:
            query = db.query(ResearchResult)

            # Apply filters
            if search_query:
                search_pattern = f"%{search_query}%"
                query = query.filter(
                    or_(
                        ResearchResult.title.ilike(search_pattern),
                        ResearchResult.content.ilike(search_pattern),
                        ResearchResult.summary.ilike(search_pattern),
                    )
                )

            if output_format:
                query = query.filter(ResearchResult.output_format == output_format)

            # Get total count
            total_count = query.count()

            # Apply pagination
            offset = (page - 1) * page_size
            results = (
                query.order_by(desc(ResearchResult.created_at))
                .offset(offset)
                .limit(page_size)
                .all()
            )

            return results, total_count

        except SQLAlchemyError as e:
            logger.error(f"Database error listing research results: {e}")
            raise

    def update_research_result(
        self,
        db: Session,
        result_id: str,
        update_data: ResearchUpdateRequest,
    ) -> Optional[ResearchResult]:
        """
        Update a research result.

        Args:
            db: Database session
            result_id: Result ID to update
            update_data: Update data

        Returns:
            Updated research result or None if not found
        """
        try:
            db_result = (
                db.query(ResearchResult).filter(ResearchResult.result_id == result_id).first()
            )

            if not db_result:
                return None

            # Update fields if provided
            if update_data.title is not None:
                db_result.title = update_data.title
            if update_data.content is not None:
                db_result.content = update_data.content
            if update_data.summary is not None:
                db_result.summary = update_data.summary
            if update_data.key_concepts is not None:
                db_result.key_concepts = update_data.key_concepts

            db_result.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(db_result)

            logger.info(f"Updated research result: {result_id}")
            return db_result

        except SQLAlchemyError as e:
            logger.error(f"Database error updating research result {result_id}: {e}")
            db.rollback()
            raise

    def delete_research_result(self, db: Session, result_id: str) -> bool:
        """
        Delete a research result.

        Args:
            db: Database session
            result_id: Result ID to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            db_result = (
                db.query(ResearchResult).filter(ResearchResult.result_id == result_id).first()
            )

            if not db_result:
                return False

            db.delete(db_result)
            db.commit()

            logger.info(f"Deleted research result: {result_id}")
            return True

        except SQLAlchemyError as e:
            logger.error(f"Database error deleting research result {result_id}: {e}")
            db.rollback()
            raise

    def list_research_sessions(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        status_filter: Optional[ResearchStatus] = None,
    ) -> tuple[List[ResearchSession], int]:
        """
        List research sessions with pagination and filtering.

        Args:
            db: Database session
            page: Page number (1-based)
            page_size: Number of items per page
            status_filter: Optional status filter

        Returns:
            Tuple of (sessions, total_count)
        """
        try:
            query = db.query(ResearchSession)

            if status_filter:
                query = query.filter(ResearchSession.status == status_filter)

            # Get total count
            total_count = query.count()

            # Apply pagination
            offset = (page - 1) * page_size
            sessions = (
                query.order_by(desc(ResearchSession.created_at))
                .offset(offset)
                .limit(page_size)
                .all()
            )

            return sessions, total_count

        except SQLAlchemyError as e:
            logger.error(f"Database error listing research sessions: {e}")
            raise

    def create_agent_activity(
        self,
        db: Session,
        session_id: str,
        agent_name: str,
        agent_type: str,
        step_name: str,
        step_order: int,
        input_data: Optional[Dict[str, Any]] = None,
        step_metadata: Optional[Dict[str, Any]] = None,
    ) -> AgentActivity:
        """
        Create a new agent activity record.

        Args:
            db: Database session
            session_id: Research session ID
            agent_name: Name of the agent
            agent_type: Type/class of the agent
            step_name: Name of the step being performed
            step_order: Order of execution
            input_data: Input data for the step
            step_metadata: Additional metadata

        Returns:
            Created agent activity
        """
        try:
            activity = AgentActivity(
                session_id=session_id,
                agent_name=agent_name,
                agent_type=agent_type,
                step_name=step_name,
                step_order=step_order,
                status="pending",
                input_data=input_data,
                step_metadata=step_metadata,
            )

            db.add(activity)
            db.commit()
            db.refresh(activity)

            logger.info(f"Created agent activity: {activity.activity_id}")
            return activity

        except SQLAlchemyError as e:
            logger.error(f"Database error creating agent activity: {e}")
            db.rollback()
            raise

    def update_agent_activity(
        self,
        db: Session,
        activity_id: str,
        status: Optional[str] = None,
        output_data: Optional[Dict[str, Any]] = None,
        sources: Optional[List[str]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        duration_seconds: Optional[int] = None,
        error_message: Optional[str] = None,
        retry_count: Optional[int] = None,
    ) -> Optional[AgentActivity]:
        """
        Update an existing agent activity record.

        Args:
            db: Database session
            activity_id: Activity ID to update
            status: New status
            output_data: Output data from the step
            sources: Sources used by the agent
            start_time: Step start time
            end_time: Step end time
            duration_seconds: Duration in seconds
            error_message: Error message if failed
            retry_count: Number of retries

        Returns:
            Updated agent activity or None if not found
        """
        try:
            activity = (
                db.query(AgentActivity).filter(AgentActivity.activity_id == activity_id).first()
            )

            if not activity:
                logger.warning(f"Agent activity not found: {activity_id}")
                return None

            # Update fields if provided
            if status is not None:
                activity.status = status
            if output_data is not None:
                activity.output_data = output_data
            if sources is not None:
                activity.sources = sources
            if start_time is not None:
                activity.start_time = start_time
            if end_time is not None:
                activity.end_time = end_time
            if duration_seconds is not None:
                activity.duration_seconds = duration_seconds
            if error_message is not None:
                activity.error_message = error_message
            if retry_count is not None:
                activity.retry_count = retry_count

            db.commit()
            db.refresh(activity)

            logger.info(f"Updated agent activity: {activity_id}")
            return activity

        except SQLAlchemyError as e:
            logger.error(f"Database error updating agent activity {activity_id}: {e}")
            db.rollback()
            raise

    def get_agent_activities(self, db: Session, session_id: str) -> List[AgentActivity]:
        """
        Get all agent activities for a research session.

        Args:
            db: Database session
            session_id: Research session ID

        Returns:
            List of agent activities
        """
        try:
            activities = (
                db.query(AgentActivity)
                .filter(AgentActivity.session_id == session_id)
                .order_by(AgentActivity.step_order, AgentActivity.start_time)
                .all()
            )

            return activities

        except SQLAlchemyError as e:
            logger.error(f"Database error getting agent activities for session {session_id}: {e}")
            raise

    def delete_agent_activities(self, db: Session, session_id: str) -> bool:
        """
        Delete all agent activities for a research session.

        Args:
            db: Database session
            session_id: Research session ID

        Returns:
            True if successful
        """
        try:
            deleted_count = (
                db.query(AgentActivity).filter(AgentActivity.session_id == session_id).delete()
            )

            db.commit()
            logger.info(f"Deleted {deleted_count} agent activities for session: {session_id}")
            return True

        except SQLAlchemyError as e:
            logger.error(f"Database error deleting agent activities for session {session_id}: {e}")
            db.rollback()
            raise


# Global database service instance
database_service = DatabaseService()
