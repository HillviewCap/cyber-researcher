"""
SQLAlchemy database models for Cyber-Researcher.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    JSON,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from .base import Base


class ResearchStatusEnum(enum.Enum):
    """Research session status enum."""

    PENDING = "pending"
    INITIALIZING = "initializing"
    RESEARCHING = "researching"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class OutputFormatEnum(enum.Enum):
    """Output format enum."""

    BLOG_POST = "blog_post"
    BOOK_CHAPTER = "book_chapter"
    RESEARCH_REPORT = "research_report"
    INTERACTIVE_SESSION = "interactive_session"


class TechnicalDepthEnum(enum.Enum):
    """Technical depth enum."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class TargetAudienceEnum(enum.Enum):
    """Target audience enum."""

    GENERAL_PUBLIC = "general_public"
    CYBERSECURITY_PROFESSIONALS = "cybersecurity_professionals"
    STUDENTS = "students"
    EXECUTIVES = "executives"
    TECHNICAL_TEAMS = "technical_teams"


class ResearchSession(Base):
    """Research session database model."""

    __tablename__ = "research_sessions"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))

    # Request fields
    topic = Column(String, nullable=False)
    content_directions = Column(Text, nullable=False)
    output_format = Column(
        SQLEnum(OutputFormatEnum), nullable=False, default=OutputFormatEnum.BLOG_POST
    )
    target_audience = Column(
        SQLEnum(TargetAudienceEnum),
        nullable=False,
        default=TargetAudienceEnum.CYBERSECURITY_PROFESSIONALS,
    )
    technical_depth = Column(
        SQLEnum(TechnicalDepthEnum), nullable=False, default=TechnicalDepthEnum.INTERMEDIATE
    )
    include_historical_context = Column(Boolean, default=True)
    style = Column(String, default="educational")

    # Book chapter specific fields
    chapter_number = Column(Integer, nullable=True)
    learning_objectives = Column(JSON, nullable=True)  # List[str]

    # Report specific fields
    report_type = Column(String, default="threat_assessment")
    confidentiality = Column(String, default="internal")

    # Session status
    status = Column(SQLEnum(ResearchStatusEnum), nullable=False, default=ResearchStatusEnum.PENDING)
    progress_percentage = Column(Integer, default=0)
    current_step = Column(String, default="initializing")
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    results = relationship("ResearchResult", back_populates="session", cascade="all, delete-orphan")


class ResearchResult(Base):
    """Research result database model."""

    __tablename__ = "research_results"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))

    # Foreign key to session
    session_id = Column(String, ForeignKey("research_sessions.session_id"), nullable=False)

    # Core result data
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True)  # List[str]
    agent_contributions = Column(JSON, nullable=True)  # Dict[str, Dict[str, Any]]

    # Format-specific fields
    output_format = Column(SQLEnum(OutputFormatEnum), nullable=False)
    summary = Column(Text, nullable=True)
    key_concepts = Column(JSON, nullable=True)  # List[str]
    exercises = Column(JSON, nullable=True)  # List[str]
    learning_objectives = Column(JSON, nullable=True)  # List[str]

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    session = relationship("ResearchSession", back_populates="results")
    metadata_entries = relationship(
        "ResearchMetadata", back_populates="result", cascade="all, delete-orphan"
    )


class ResearchMetadata(Base):
    """Research metadata database model."""

    __tablename__ = "research_metadata"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to result
    result_id = Column(String, ForeignKey("research_results.result_id"), nullable=False)

    # Metadata fields
    key = Column(String, nullable=False)
    value = Column(JSON, nullable=True)  # Flexible JSON storage for any metadata

    # Specific metadata types for common use cases
    tags = Column(JSON, nullable=True)  # List[str]
    categories = Column(JSON, nullable=True)  # List[str]
    custom_fields = Column(JSON, nullable=True)  # Dict[str, Any]

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    result = relationship("ResearchResult", back_populates="metadata_entries")
