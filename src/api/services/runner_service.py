"""
Service layer wrapping CyberStormRunner for API integration.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

from ...cyber_storm import CyberStormRunner, CyberStormConfig
from ...cyber_storm.agents import ContentType
from ..models.research import ResearchResult, ResearchStatus, OutputFormat

logger = logging.getLogger(__name__)


class RunnerService:
    """Service layer for CyberStormRunner API integration."""
    
    def __init__(self):
        self.runner: Optional[CyberStormRunner] = None
        self.config: Optional[CyberStormConfig] = None
        
    async def initialize(self):
        """Initialize the runner service."""
        try:
            # Load configuration
            self.config = CyberStormConfig()
            
            # Initialize runner
            self.runner = CyberStormRunner(self.config)
            
            logger.info("RunnerService initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RunnerService: {e}")
            raise
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
        if not self.runner:
            raise RuntimeError("Runner not initialized")
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        status = await loop.run_in_executor(None, self.runner.get_system_status)
        return status
    
    async def generate_blog_post(
        self,
        topic: str,
        content_directions: str,
        style: str = "educational",
        target_audience: str = "cybersecurity_professionals",
        technical_depth: str = "intermediate",
        include_historical_context: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> ResearchResult:
        """Generate a blog post."""
        
        if not self.runner:
            raise RuntimeError("Runner not initialized")
        
        # Update progress
        if progress_callback:
            await progress_callback(ResearchStatus.RESEARCHING, 30, "Security analysis in progress...")
        
        # Enhance topic with content directions
        enhanced_topic = f"{topic} - {content_directions}"
        
        # Run blog post generation in thread pool
        loop = asyncio.get_event_loop()
        blog_post = await loop.run_in_executor(
            None, 
            self.runner.generate_blog_post,
            enhanced_topic,
            style
        )
        
        if progress_callback:
            await progress_callback(ResearchStatus.GENERATING, 80, "Formatting blog post...")
        
        # Create result
        result = ResearchResult(
            session_id="",  # Will be set by caller
            title=blog_post.title,
            content=blog_post.content,
            metadata=blog_post.metadata,
            sources=blog_post.sources,
            agent_contributions=self._extract_agent_contributions(blog_post.metadata),
            created_at=datetime.fromisoformat(blog_post.created_at),
            output_format=OutputFormat.BLOG_POST,
            summary=blog_post.summary,
            tags=blog_post.tags,
        )
        
        return result
    
    async def generate_book_chapter(
        self,
        topic: str,
        content_directions: str,
        chapter_number: int = 1,
        learning_objectives: List[str] = None,
        target_audience: str = "cybersecurity_professionals",
        technical_depth: str = "intermediate",
        include_historical_context: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> ResearchResult:
        """Generate a book chapter."""
        
        if not self.runner:
            raise RuntimeError("Runner not initialized")
        
        if progress_callback:
            await progress_callback(ResearchStatus.RESEARCHING, 30, "Historical research in progress...")
        
        # Enhance topic with content directions
        enhanced_topic = f"{topic} - {content_directions}"
        objectives = learning_objectives or [
            f"Understand the key concepts of {topic}",
            f"Analyze the historical context of {topic}",
            f"Apply security principles related to {topic}",
        ]
        
        # Run chapter generation in thread pool
        loop = asyncio.get_event_loop()
        chapter = await loop.run_in_executor(
            None,
            self.runner.generate_book_chapter,
            enhanced_topic,
            chapter_number,
            objectives
        )
        
        if progress_callback:
            await progress_callback(ResearchStatus.GENERATING, 80, "Formatting book chapter...")
        
        # Create result
        result = ResearchResult(
            session_id="",  # Will be set by caller
            title=chapter.title,
            content=chapter.content,
            metadata=chapter.metadata,
            sources=chapter.sources,
            agent_contributions=self._extract_agent_contributions(chapter.metadata),
            created_at=datetime.fromisoformat(chapter.created_at),
            output_format=OutputFormat.BOOK_CHAPTER,
            summary=chapter.summary,
            key_concepts=chapter.key_concepts,
            exercises=chapter.exercises,
            learning_objectives=chapter.learning_objectives,
        )
        
        return result
    
    async def generate_research_report(
        self,
        topic: str,
        content_directions: str,
        report_type: str = "threat_assessment",
        confidentiality: str = "internal",
        target_audience: str = "cybersecurity_professionals",
        technical_depth: str = "intermediate",
        include_historical_context: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> ResearchResult:
        """Generate a research report."""
        
        if not self.runner:
            raise RuntimeError("Runner not initialized")
        
        if progress_callback:
            await progress_callback(ResearchStatus.RESEARCHING, 30, "Threat intelligence analysis...")
        
        # Enhance topic with content directions
        enhanced_topic = f"{topic} - {content_directions}"
        
        # Run report generation in thread pool
        loop = asyncio.get_event_loop()
        report = await loop.run_in_executor(
            None,
            self.runner.generate_research_report,
            enhanced_topic,
            report_type,
            confidentiality
        )
        
        if progress_callback:
            await progress_callback(ResearchStatus.GENERATING, 80, "Formatting research report...")
        
        # Create result
        result = ResearchResult(
            session_id="",  # Will be set by caller
            title=report["title"],
            content=report["content"],
            metadata=report["metadata"],
            sources=[],  # Research reports don't have sources in the same format
            agent_contributions=self._extract_agent_contributions(report["metadata"]),
            created_at=datetime.fromisoformat(report["created_at"]),
            output_format=OutputFormat.RESEARCH_REPORT,
        )
        
        return result
    
    async def create_interactive_session(
        self,
        topic: str,
        content_directions: str,
        target_audience: str = "cybersecurity_professionals",
        progress_callback: Optional[Callable] = None
    ) -> ResearchResult:
        """Create an interactive research session."""
        
        if not self.runner:
            raise RuntimeError("Runner not initialized")
        
        if progress_callback:
            await progress_callback(ResearchStatus.RESEARCHING, 50, "Creating interactive session...")
        
        # Enhance topic with content directions
        enhanced_topic = f"{topic} - {content_directions}"
        
        # Run interactive session creation in thread pool
        loop = asyncio.get_event_loop()
        session = await loop.run_in_executor(
            None,
            self.runner.interactive_research,
            enhanced_topic
        )
        
        if progress_callback:
            await progress_callback(ResearchStatus.GENERATING, 80, "Formatting session data...")
        
        # Create result
        result = ResearchResult(
            session_id="",  # Will be set by caller
            title=f"Interactive Research: {session.topic}",
            content=self._format_interactive_content(session),
            metadata={
                "session_id": session.session_id,
                "questions_generated": len(session.generated_questions),
                "insights_count": len(session.insights),
            },
            sources=[],
            agent_contributions={
                "questions": {"count": len(session.generated_questions)},
                "insights": {"count": len(session.insights)},
            },
            created_at=datetime.fromisoformat(session.created_at),
            output_format=OutputFormat.INTERACTIVE_SESSION,
        )
        
        return result
    
    def _extract_agent_contributions(self, metadata: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Extract agent contributions from metadata."""
        contributions = {}
        
        agents_used = metadata.get("agents_used", [])
        for agent in agents_used:
            contributions[agent] = {
                "status": "completed",
                "contribution_type": agent.replace("_", " ").title(),
            }
        
        return contributions
    
    def _format_interactive_content(self, session) -> str:
        """Format interactive session content."""
        content_parts = [
            f"# Interactive Research Session: {session.topic}\n",
            f"**Session ID:** {session.session_id}\n",
            f"**Created:** {session.created_at}\n\n",
            "## Generated Research Questions\n",
        ]
        
        for i, question in enumerate(session.generated_questions, 1):
            content_parts.append(f"{i}. {question}\n")
        
        content_parts.extend([
            "\n## Insights\n",
            *[f"- {insight}\n" for insight in session.insights],
            "\n## Conversation Log\n",
        ])
        
        for entry in session.conversation_log:
            content_parts.append(f"**{entry.get('type', 'entry')}:** {entry.get('content', '')}\n")
        
        return "".join(content_parts)