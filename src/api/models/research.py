"""
Pydantic models for research API endpoints.
"""

from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class OutputFormat(str, Enum):
    """Available output formats."""

    BLOG_POST = "blog_post"
    BOOK_CHAPTER = "book_chapter"
    RESEARCH_REPORT = "research_report"
    INTERACTIVE_SESSION = "interactive_session"


class TechnicalDepth(str, Enum):
    """Technical depth levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class TargetAudience(str, Enum):
    """Target audience types."""

    GENERAL_PUBLIC = "general_public"
    CYBERSECURITY_PROFESSIONALS = "cybersecurity_professionals"
    STUDENTS = "students"
    EXECUTIVES = "executives"
    TECHNICAL_TEAMS = "technical_teams"


class ResearchRequest(BaseModel):
    """Request model for starting research."""

    topic: str = Field(..., description="Main research topic/title")
    content_directions: str = Field(
        ..., description="Specific content directions and insights to explore"
    )
    output_format: OutputFormat = Field(
        default=OutputFormat.BLOG_POST, description="Desired output format"
    )
    target_audience: TargetAudience = Field(
        default=TargetAudience.CYBERSECURITY_PROFESSIONALS,
        description="Target audience for the content",
    )
    technical_depth: TechnicalDepth = Field(
        default=TechnicalDepth.INTERMEDIATE, description="Technical depth level"
    )
    include_historical_context: bool = Field(
        default=True, description="Whether to include historical context"
    )
    style: str = Field(
        default="educational", description="Writing style (educational, technical, narrative)"
    )
    # Book chapter specific fields
    chapter_number: Optional[int] = Field(
        default=None, description="Chapter number (for book chapter format)"
    )
    learning_objectives: Optional[List[str]] = Field(
        default=None, description="Learning objectives (for book chapter format)"
    )
    # Report specific fields
    report_type: Optional[str] = Field(
        default="threat_assessment", description="Report type (for research report format)"
    )
    confidentiality: Optional[str] = Field(
        default="internal", description="Confidentiality level (for research report format)"
    )


class ResearchStatus(str, Enum):
    """Research session status."""

    PENDING = "pending"
    INITIALIZING = "initializing"
    RESEARCHING = "researching"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ProgressUpdate(BaseModel):
    """Progress update model."""

    session_id: str
    status: ResearchStatus
    progress_percentage: int = Field(ge=0, le=100)
    current_step: str
    estimated_completion: Optional[datetime] = None
    agent_activity: Dict[str, str] = Field(default_factory=dict)


class ResearchResult(BaseModel):
    """Research result model."""

    session_id: str
    title: str
    content: str
    metadata: Dict[str, Any]
    sources: List[str]
    agent_contributions: Dict[str, Dict[str, Any]]
    created_at: datetime
    output_format: OutputFormat

    # Format-specific fields
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    key_concepts: Optional[List[str]] = None
    exercises: Optional[List[str]] = None
    learning_objectives: Optional[List[str]] = None


class ResearchSession(BaseModel):
    """Research session model."""

    session_id: str
    request: ResearchRequest
    status: ResearchStatus
    created_at: datetime
    updated_at: datetime
    progress_percentage: int = 0
    current_step: str = "initializing"
    result: Optional[ResearchResult] = None
    error_message: Optional[str] = None


class StartResearchResponse(BaseModel):
    """Response for starting research."""

    session_id: str
    status: ResearchStatus
    message: str


class SystemStatus(BaseModel):
    """System status model."""

    agents: Dict[str, str]
    retrieval: Dict[str, str]
    configuration: Dict[str, Any]
    output_directory: str


# Database operation models
class ResearchSessionDB(BaseModel):
    """Database representation of research session."""

    model_config = {"from_attributes": True}

    id: int
    session_id: str
    topic: str
    content_directions: str
    output_format: OutputFormat
    target_audience: TargetAudience
    technical_depth: TechnicalDepth
    include_historical_context: bool
    style: str
    chapter_number: Optional[int] = None
    learning_objectives: Optional[List[str]] = None
    report_type: Optional[str] = None
    confidentiality: Optional[str] = None
    status: ResearchStatus
    progress_percentage: int
    current_step: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ResearchResultDB(BaseModel):
    """Database representation of research result."""

    model_config = {"from_attributes": True}

    id: int
    result_id: str
    session_id: str
    title: str
    content: str
    sources: Optional[List[str]] = None
    agent_contributions: Optional[Dict[str, Dict[str, Any]]] = None
    output_format: OutputFormat
    summary: Optional[str] = None
    key_concepts: Optional[List[str]] = None
    exercises: Optional[List[str]] = None
    learning_objectives: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime


class ResearchListResponse(BaseModel):
    """Response model for listing research results."""

    total: int
    page: int
    page_size: int
    items: List[ResearchResultDB]


class ResearchUpdateRequest(BaseModel):
    """Request model for updating research results."""

    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    key_concepts: Optional[List[str]] = None


class ResearchDeleteResponse(BaseModel):
    """Response model for deleting research results."""

    success: bool
    message: str
    deleted_result_id: str
