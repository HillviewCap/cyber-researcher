"""
Main CyberStormRunner class for Cyber-Researcher.

This module provides the main orchestration class that coordinates
the various agents and modules to generate cybersecurity narratives.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

from knowledge_storm.rm import (
    BingSearch,
    DuckDuckGoSearchRM,
    YouRM,
    SerperRM,
    BraveRM,
    TavilySearchRM,
)

from .config import CyberStormConfig
from .agents import (
    SecurityAnalystAgent,
    ThreatResearcherAgent,
    HistorianAgent,
    AgentContext,
    AgentResponse,
    ContentType,
)
from .rm import ThreatIntelRM, HistoricalRM
from .templates import BlogPostTemplate, BookChapterTemplate, ResearchReportTemplate
from .modules import title_generator
from .workflow_tracker import WorkflowTracker


@dataclass
class BlogPost:
    """Structure for generated blog posts."""

    title: str
    content: str  # Final polished content only
    summary: str
    tags: List[str]
    sources: List[str]
    metadata: Dict[str, Any]  # Technical metadata
    workflow_metadata: Dict[str, Any]  # Agent workflow and process information
    generation_process: Dict[str, Any]  # Step-by-step generation process
    agent_workflow_summary: Dict[str, Any]  # Summary of agent activities
    created_at: str


@dataclass
class BookChapter:
    """Structure for generated book chapters."""

    chapter_number: int
    title: str
    content: str  # Final polished content only
    summary: str
    learning_objectives: List[str]
    key_concepts: List[str]
    exercises: List[str]
    sources: List[str]
    metadata: Dict[str, Any]  # Technical metadata
    workflow_metadata: Dict[str, Any]  # Agent workflow and process information
    generation_process: Dict[str, Any]  # Step-by-step generation process
    agent_workflow_summary: Dict[str, Any]  # Summary of agent activities
    created_at: str


@dataclass
class InteractiveSession:
    """Structure for interactive research sessions."""

    topic: str
    conversation_log: List[Dict[str, Any]]
    generated_questions: List[str]
    insights: List[str]
    session_id: str
    created_at: str


class CyberStormRunner:
    """
    Main orchestration class for Cyber-Researcher.

    This class coordinates the various agents and modules to generate
    cybersecurity narratives that blend historical context with technical content.
    """

    def __init__(self, config: Optional[CyberStormConfig] = None):
        """
        Initialize the CyberStormRunner.

        Args:
            config: Configuration object. If None, uses default configuration.
        """
        self.config = config or CyberStormConfig()

        # Validate configuration
        issues = self.config.validate_config()
        if issues:
            print("Configuration issues found:")
            for issue in issues:
                print(f"  - {issue}")
            print("Some features may not work properly.")

        # Initialize agents
        self._init_agents()

        # Initialize retrieval modules
        self._init_retrieval_modules()

        # Initialize output directory
        self._init_output_directory()

        # Initialize templates
        self._init_templates()

    def _init_agents(self):
        """Initialize the three main agents."""
        try:
            # Security Analyst Agent
            self.security_analyst = SecurityAnalystAgent(
                language_model=self.config.get_lm_for_agent("security_analyst"),
                config=self.config.security_analyst_config.lm_config.__dict__,
            )

            # Threat Researcher Agent
            self.threat_researcher = ThreatResearcherAgent(
                language_model=self.config.get_lm_for_agent("threat_researcher"),
                config=self.config.threat_researcher_config.lm_config.__dict__,
            )

            # Historian Agent
            self.historian = HistorianAgent(
                language_model=self.config.get_lm_for_agent("historian"),
                config=self.config.historian_config.lm_config.__dict__,
            )

            print("✓ Agents initialized successfully")

        except Exception as e:
            print(f"Error initializing agents: {e}")
            raise

    def _init_retrieval_modules(self):
        """Initialize retrieval modules."""
        try:
            # Web search retrieval
            search_engine = self.config.retrieval_config.search_engine
            api_key = self.config.get_search_api_key(search_engine)

            if search_engine == "bing" and api_key:
                self.web_retrieval = BingSearch(
                    bing_search_api=api_key, k=self.config.retrieval_config.max_results_per_query
                )
            elif search_engine == "you" and api_key:
                self.web_retrieval = YouRM(
                    ydc_api_key=api_key, k=self.config.retrieval_config.max_results_per_query
                )
            elif search_engine == "serper" and api_key:
                self.web_retrieval = SerperRM(
                    serper_search_api_key=api_key,
                    k=self.config.retrieval_config.max_results_per_query,
                )
            elif search_engine == "duckduckgo":
                self.web_retrieval = DuckDuckGoSearchRM(
                    k=self.config.retrieval_config.max_results_per_query
                )
            else:
                print(
                    f"Warning: No valid configuration for search engine '{search_engine}', using DuckDuckGo"
                )
                self.web_retrieval = DuckDuckGoSearchRM(
                    k=self.config.retrieval_config.max_results_per_query
                )

            # Threat intelligence retrieval
            self.threat_intel_rm = ThreatIntelRM(
                collection_name="threat_intelligence",
                embedding_model=self.config.retrieval_config.embedding_model,
                device=self.config.retrieval_config.device,
                k=self.config.retrieval_config.max_results_per_query,
                vector_store_path=self.config.retrieval_config.vector_store_path,
                qdrant_url=self.config.retrieval_config.qdrant_url,
                qdrant_api_key=self.config.retrieval_config.qdrant_api_key,
            )

            # Historical context retrieval
            self.historical_rm = HistoricalRM(
                collection_name="historical_context",
                embedding_model=self.config.retrieval_config.embedding_model,
                device=self.config.retrieval_config.device,
                k=self.config.retrieval_config.max_results_per_query,
                vector_store_path=self.config.retrieval_config.vector_store_path,
                qdrant_url=self.config.retrieval_config.qdrant_url,
                qdrant_api_key=self.config.retrieval_config.qdrant_api_key,
            )

            # Set retrieval modules for agents
            self.security_analyst.retrieval_module = self.web_retrieval
            self.threat_researcher.retrieval_module = self.threat_intel_rm
            self.historian.retrieval_module = self.historical_rm

            print("✓ Retrieval modules initialized successfully")

        except Exception as e:
            print(f"Error initializing retrieval modules: {e}")
            # Continue with limited functionality
            self.web_retrieval = None
            self.threat_intel_rm = None
            self.historical_rm = None

    def _init_output_directory(self):
        """Initialize output directory."""
        output_dir = Path(self.config.output_config.output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = output_dir

    def _init_templates(self):
        """Initialize content templates."""
        try:
            self.blog_template = BlogPostTemplate()
            self.chapter_template = BookChapterTemplate()
            self.report_template = ResearchReportTemplate()
            print("✓ Content templates initialized successfully")
        except Exception as e:
            print(f"Error initializing templates: {e}")
            # Fall back to basic templates
            self.blog_template = None
            self.chapter_template = None
            self.report_template = None

    def generate_blog_post(
        self, topic: str, style: str = "educational", session_id: str = None
    ) -> BlogPost:
        """
        Generate a blog post on a cybersecurity topic with workflow tracking.

        Args:
            topic: The cybersecurity topic to write about
            style: Writing style (educational, technical, narrative)
            session_id: Optional session ID for workflow tracking

        Returns:
            BlogPost object with generated content and workflow metadata
        """
        print(f"Generating blog post on: {topic}")

        # Initialize workflow tracker
        if not session_id:
            session_id = f"blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        tracker = WorkflowTracker(session_id)

        # Create agent context
        context = AgentContext(
            topic=topic,
            content_type=ContentType.BLOG_POST,
            target_audience=self.config.generation_config.default_audience,
            technical_depth=self.config.generation_config.default_technical_depth,
            narrative_style=style,
            historical_focus=self.config.generation_config.include_historical_context,
        )

        # Track agent activities
        try:
            # Security Analyst Phase
            security_activity = tracker.start_activity(
                agent_name="security_analyst",
                agent_type="SecurityAnalystAgent",
                step_name="analyze_topic",
                input_data={"topic": topic, "context": context.__dict__},
            )
            security_analysis = self.security_analyst.analyze_topic(context)
            tracker.complete_activity(
                security_activity,
                output_data={
                    "content_length": len(security_analysis.content),
                    "suggestions_count": len(security_analysis.suggestions),
                },
                sources=security_analysis.sources,
            )

            # Threat Researcher Phase
            threat_activity = tracker.start_activity(
                agent_name="threat_researcher",
                agent_type="ThreatResearcherAgent",
                step_name="analyze_topic",
                input_data={"topic": topic, "context": context.__dict__},
            )
            threat_analysis = self.threat_researcher.analyze_topic(context)
            tracker.complete_activity(
                threat_activity,
                output_data={
                    "content_length": len(threat_analysis.content),
                    "suggestions_count": len(threat_analysis.suggestions),
                },
                sources=threat_analysis.sources,
            )

            # Historian Phase
            historian_activity = tracker.start_activity(
                agent_name="historian",
                agent_type="HistorianAgent",
                step_name="analyze_topic",
                input_data={"topic": topic, "context": context.__dict__},
            )
            historical_analysis = self.historian.analyze_topic(context)
            tracker.complete_activity(
                historian_activity,
                output_data={
                    "content_length": len(historical_analysis.content),
                    "suggestions_count": len(historical_analysis.suggestions),
                },
                sources=historical_analysis.sources,
            )

            # Content Synthesis Phase
            synthesis_activity = tracker.start_activity(
                agent_name="content_synthesizer",
                agent_type="ContentSynthesizer",
                step_name="synthesize_blog_content",
                input_data={"style": style, "template_available": self.blog_template is not None},
            )

            # Generate technical metadata (separate from workflow)
            metadata = {
                "style": style,
                "technical_depth": context.technical_depth,
                "target_audience": context.target_audience,
                "content_type": "blog_post",
            }

            # Synthesize content using professional template
            if self.blog_template:
                # Generate preliminary content for title analysis
                preliminary_content = self.blog_template.format_blog_post(
                    title=topic,  # Temporary title for content generation
                    topic=topic,
                    security_analysis=security_analysis.content,
                    threat_analysis=threat_analysis.content,
                    historical_analysis=historical_analysis.content,
                    suggestions=security_analysis.suggestions
                    + threat_analysis.suggestions
                    + historical_analysis.suggestions,
                    sources=list(
                        set(
                            security_analysis.sources
                            + threat_analysis.sources
                            + historical_analysis.sources
                        )
                    ),
                    metadata=metadata,
                    style=style,
                )

                # Generate optimized title based on content
                title = title_generator.generate_title(
                    topic=topic,
                    content=preliminary_content[:1000],  # First 1000 chars for analysis
                    content_type="blog_post",
                )

                # Re-generate content with optimized title (FINAL CLEAN CONTENT)
                content = self.blog_template.format_blog_post(
                    title=title,
                    topic=topic,
                    security_analysis=security_analysis.content,
                    threat_analysis=threat_analysis.content,
                    historical_analysis=historical_analysis.content,
                    suggestions=security_analysis.suggestions
                    + threat_analysis.suggestions
                    + historical_analysis.suggestions,
                    sources=list(
                        set(
                            security_analysis.sources
                            + threat_analysis.sources
                            + historical_analysis.sources
                        )
                    ),
                    metadata=metadata,
                    style=style,
                )
            else:
                # Fallback to basic synthesis
                content = self._synthesize_blog_content(
                    topic, security_analysis, threat_analysis, historical_analysis
                )

                # Generate title for fallback content
                title = title_generator.generate_title(
                    topic=topic, content=content[:1000], content_type="blog_post"
                )

            tracker.complete_activity(
                synthesis_activity,
                output_data={
                    "final_content_length": len(content),
                    "title": title,
                    "template_used": self.blog_template is not None,
                },
            )

            # Collect all sources
            all_sources = list(
                set(
                    security_analysis.sources
                    + threat_analysis.sources
                    + historical_analysis.sources
                )
            )

        except Exception as e:
            # Handle any activity failures
            for activity_id in tracker.current_activities:
                tracker.fail_activity(activity_id, str(e))
            raise

        # Get workflow data for metadata separation
        workflow_metadata = tracker.get_workflow_metadata()
        generation_process = tracker.get_generation_process()
        agent_workflow_summary = tracker.get_agent_contributions_summary()

        # Create blog post with separated content and workflow metadata
        blog_post = BlogPost(
            title=title,
            content=content,  # ONLY final polished content, no workflow info
            summary=self._generate_summary(content),
            tags=self._extract_tags(topic, content),
            sources=all_sources,
            metadata=metadata,  # Technical metadata only
            workflow_metadata=workflow_metadata,  # Complete workflow information
            generation_process=generation_process,  # Step-by-step process
            agent_workflow_summary=agent_workflow_summary,  # Agent contributions summary
            created_at=datetime.now().isoformat(),
        )

        # Save blog post
        if self.config.output_config.save_intermediate_results:
            self._save_blog_post(blog_post)

        print("✓ Blog post generated successfully")
        return blog_post

    def generate_book_chapter(
        self, topic: str, chapter_num: int, learning_objectives: List[str]
    ) -> BookChapter:
        """
        Generate a book chapter on a cybersecurity topic.

        Args:
            topic: The cybersecurity topic
            chapter_num: Chapter number
            learning_objectives: List of learning objectives

        Returns:
            BookChapter object with generated content
        """
        print(f"Generating book chapter {chapter_num} on: {topic}")

        # Create agent context
        context = AgentContext(
            topic=topic,
            content_type=ContentType.BOOK_CHAPTER,
            target_audience=self.config.generation_config.default_audience,
            technical_depth=self.config.generation_config.default_technical_depth,
            historical_focus=self.config.generation_config.include_historical_context,
        )

        # Get analysis from all agents
        security_analysis = self.security_analyst.analyze_topic(context)
        threat_analysis = self.threat_researcher.analyze_topic(context)
        historical_analysis = self.historian.analyze_topic(context)

        # Synthesize content using professional template
        if self.chapter_template:
            # Generate preliminary content for title analysis
            preliminary_content = self.chapter_template.format_book_chapter(
                chapter_number=chapter_num,
                title=f"Chapter {chapter_num}: {topic}",  # Temporary title
                topic=topic,
                learning_objectives=learning_objectives,
                security_analysis=security_analysis.content,
                threat_analysis=threat_analysis.content,
                historical_analysis=historical_analysis.content,
                suggestions=security_analysis.suggestions
                + threat_analysis.suggestions
                + historical_analysis.suggestions,
                sources=list(
                    set(
                        security_analysis.sources
                        + threat_analysis.sources
                        + historical_analysis.sources
                    )
                ),
                metadata={
                    "agents_used": ["security_analyst", "threat_researcher", "historian"],
                    "technical_depth": context.technical_depth,
                    "target_audience": context.target_audience,
                },
            )

            # Generate optimized title based on content
            chapter_title = title_generator.generate_title(
                topic=topic,
                content=preliminary_content[:1000],
                content_type="book_chapter",
                chapter_number=chapter_num,
            )

            # Re-generate content with optimized title
            content = self.chapter_template.format_book_chapter(
                chapter_number=chapter_num,
                title=chapter_title,
                topic=topic,
                learning_objectives=learning_objectives,
                security_analysis=security_analysis.content,
                threat_analysis=threat_analysis.content,
                historical_analysis=historical_analysis.content,
                suggestions=security_analysis.suggestions
                + threat_analysis.suggestions
                + historical_analysis.suggestions,
                sources=list(
                    set(
                        security_analysis.sources
                        + threat_analysis.sources
                        + historical_analysis.sources
                    )
                ),
                metadata={
                    "agents_used": ["security_analyst", "threat_researcher", "historian"],
                    "technical_depth": context.technical_depth,
                    "target_audience": context.target_audience,
                },
            )
        else:
            # Fallback to basic synthesis
            content = self._synthesize_chapter_content(
                topic, security_analysis, threat_analysis, historical_analysis, learning_objectives
            )

        # Generate exercises and key concepts
        exercises = self._generate_exercises(topic, learning_objectives)
        key_concepts = self._extract_key_concepts(content)

        # Create book chapter
        book_chapter = BookChapter(
            chapter_number=chapter_num,
            title=f"Chapter {chapter_num}: {topic}",
            content=content,
            summary=self._generate_summary(content),
            learning_objectives=learning_objectives,
            key_concepts=key_concepts,
            exercises=exercises,
            sources=list(
                set(
                    security_analysis.sources
                    + threat_analysis.sources
                    + historical_analysis.sources
                )
            ),
            metadata={
                "agents_used": ["security_analyst", "threat_researcher", "historian"],
                "word_count": len(content.split()),
                "technical_depth": context.technical_depth,
            },
            created_at=datetime.now().isoformat(),
        )

        # Save chapter
        if self.config.output_config.save_intermediate_results:
            self._save_book_chapter(book_chapter)

        print("✓ Book chapter generated successfully")
        return book_chapter

    def interactive_research(self, topic: str) -> InteractiveSession:
        """
        Start an interactive research session.

        Args:
            topic: The research topic

        Returns:
            InteractiveSession object
        """
        print(f"Starting interactive research session on: {topic}")

        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create agent context
        context = AgentContext(
            topic=topic,
            content_type=ContentType.RESEARCH_REPORT,
            target_audience=self.config.generation_config.default_audience,
        )

        # Generate initial questions from all agents
        security_questions = self.security_analyst.generate_questions(context)
        threat_questions = self.threat_researcher.generate_questions(context)
        historical_questions = self.historian.generate_questions(context)

        all_questions = security_questions + threat_questions + historical_questions

        # Initial conversation log
        conversation_log = [
            {
                "timestamp": datetime.now().isoformat(),
                "type": "initialization",
                "content": f"Research session started for topic: {topic}",
                "questions_generated": len(all_questions),
            }
        ]

        session = InteractiveSession(
            topic=topic,
            conversation_log=conversation_log,
            generated_questions=all_questions,
            insights=[],
            session_id=session_id,
            created_at=datetime.now().isoformat(),
        )

        print(
            f"✓ Interactive session '{session_id}' created with {len(all_questions)} research questions"
        )
        return session

    def generate_research_report(
        self, topic: str, report_type: str = "threat_assessment", confidentiality: str = "internal"
    ) -> Dict[str, Any]:
        """
        Generate a professional research report on a cybersecurity topic.

        Args:
            topic: The cybersecurity topic to analyze
            report_type: Type of report (threat_assessment, incident_analysis, etc.)
            confidentiality: Report confidentiality level

        Returns:
            Dictionary containing the formatted report and metadata
        """
        print(f"Generating research report on: {topic}")

        # Create agent context
        context = AgentContext(
            topic=topic,
            content_type=ContentType.RESEARCH_REPORT,
            target_audience="cybersecurity professionals",
            technical_depth="advanced",
            historical_focus=True,
        )

        # Get analysis from all agents
        security_analysis = self.security_analyst.analyze_topic(context)
        threat_analysis = self.threat_researcher.analyze_topic(context)
        historical_analysis = self.historian.analyze_topic(context)

        # Extract key findings and recommendations
        key_findings = (
            security_analysis.suggestions[:3]
            + threat_analysis.suggestions[:3]
            + historical_analysis.suggestions[:3]
        )

        recommendations = (
            security_analysis.suggestions
            + threat_analysis.suggestions
            + historical_analysis.suggestions
        )

        sources = list(
            set(security_analysis.sources + threat_analysis.sources + historical_analysis.sources)
        )

        # Generate professional report using template
        if self.report_template:
            from .templates.report_template import ReportMetadata, ReportType, ConfidentialityLevel

            # Map string parameters to enums
            report_type_enum = getattr(
                ReportType, report_type.upper(), ReportType.THREAT_ASSESSMENT
            )
            confidentiality_enum = getattr(
                ConfidentialityLevel, confidentiality.upper(), ConfidentialityLevel.INTERNAL
            )

            # Generate preliminary content for title analysis
            preliminary_summary = f"This report provides comprehensive analysis of {topic} from multiple cybersecurity perspectives, integrating historical context with current threat intelligence and defensive security recommendations."

            # Generate optimized title based on content and report type
            optimized_title = title_generator.generate_title(
                topic=topic,
                content=security_analysis.content[:500] + threat_analysis.content[:500],
                content_type="research_report",
                report_type=report_type,
            )

            metadata = ReportMetadata(
                title=optimized_title,
                report_type=report_type_enum,
                confidentiality=confidentiality_enum,
                authors=["Cyber-Researcher Analysis Team"],
                date=datetime.now().strftime("%Y-%m-%d"),
                version="1.0",
                distribution_list=["Security Team", "Executive Leadership"],
            )

            executive_summary = f"This report provides comprehensive analysis of {topic} from multiple cybersecurity perspectives, integrating historical context with current threat intelligence and defensive security recommendations."

            report_content = self.report_template.format_research_report(
                metadata=metadata,
                executive_summary=executive_summary,
                security_analysis=security_analysis.content,
                threat_analysis=threat_analysis.content,
                historical_analysis=historical_analysis.content,
                key_findings=key_findings,
                recommendations=recommendations,
                sources=sources,
                additional_metadata={
                    "agents_used": ["security_analyst", "threat_researcher", "historian"],
                    "technical_depth": context.technical_depth,
                    "analysis_date": datetime.now().isoformat(),
                },
            )

            report_data = {
                "title": metadata.title,
                "content": report_content,
                "metadata": {
                    "report_type": report_type,
                    "confidentiality": confidentiality,
                    "authors": metadata.authors,
                    "date": metadata.date,
                    "version": metadata.version,
                    "key_findings_count": len(key_findings),
                    "recommendations_count": len(recommendations),
                    "sources_count": len(sources),
                },
                "created_at": datetime.now().isoformat(),
            }
        else:
            # Fallback to basic report structure
            report_content = self._synthesize_basic_report(
                topic, security_analysis, threat_analysis, historical_analysis
            )

            report_data = {
                "title": f"Cybersecurity Analysis: {topic}",
                "content": report_content,
                "metadata": {
                    "report_type": report_type,
                    "confidentiality": confidentiality,
                    "key_findings_count": len(key_findings),
                    "recommendations_count": len(recommendations),
                    "sources_count": len(sources),
                },
                "created_at": datetime.now().isoformat(),
            }

        # Save report if configured
        if self.config.output_config.save_intermediate_results:
            self._save_research_report(report_data)

        print("✓ Research report generated successfully")
        return report_data

    def ingest_threat_report(self, report_path: str) -> bool:
        """
        Add a threat intelligence report to the knowledge base.

        Args:
            report_path: Path to the threat report file

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.threat_intel_rm is None:
                print("Error: Threat intelligence retrieval module not initialized")
                return False

            num_reports = self.threat_intel_rm.ingest_threat_reports(report_path)
            print(f"✓ Successfully ingested {num_reports} threat reports")
            return True

        except Exception as e:
            print(f"Error ingesting threat report: {e}")
            return False

    def _synthesize_blog_content(
        self,
        topic: str,
        security_analysis: AgentResponse,
        threat_analysis: AgentResponse,
        historical_analysis: AgentResponse,
    ) -> str:
        """Synthesize content from all agent analyses into a blog post."""

        content_parts = [
            f"# {topic}: A Comprehensive Analysis\n",
            "## Introduction\n",
            f"In the ever-evolving landscape of cybersecurity, understanding {topic} requires examining it from multiple perspectives. ",
            "This analysis combines defensive security insights, threat intelligence, and historical context to provide a comprehensive view.\n",
            "## Historical Context\n",
            historical_analysis.content + "\n",
            "## Security Analysis\n",
            security_analysis.content + "\n",
            "## Threat Intelligence Perspective\n",
            threat_analysis.content + "\n",
            "## Key Takeaways\n",
            "- " + "\n- ".join(security_analysis.suggestions[:3]) + "\n",
            "- " + "\n- ".join(threat_analysis.suggestions[:3]) + "\n",
            "- " + "\n- ".join(historical_analysis.suggestions[:3]) + "\n",
            "## Conclusion\n",
            f"Understanding {topic} requires a multi-faceted approach that combines technical knowledge, ",
            "threat awareness, and historical perspective. By learning from the past and staying current with emerging threats, ",
            "cybersecurity professionals can better protect their organizations and adapt to future challenges.",
        ]

        return "\n".join(content_parts)

    def _synthesize_chapter_content(
        self,
        topic: str,
        security_analysis: AgentResponse,
        threat_analysis: AgentResponse,
        historical_analysis: AgentResponse,
        learning_objectives: List[str],
    ) -> str:
        """Synthesize content from all agent analyses into a book chapter."""

        content_parts = [
            f"# {topic}\n",
            "## Learning Objectives\n",
            "By the end of this chapter, you will be able to:\n",
            "\n".join([f"- {obj}" for obj in learning_objectives]) + "\n",
            "## Introduction\n",
            f"This chapter explores {topic} from multiple perspectives, combining historical insights, ",
            "defensive security principles, and threat intelligence to provide a comprehensive understanding.\n",
            "## Historical Foundation\n",
            historical_analysis.content + "\n",
            "## Security Architecture and Defense\n",
            security_analysis.content + "\n",
            "## Threat Landscape and Intelligence\n",
            threat_analysis.content + "\n",
            "## Practical Applications\n",
            "### Implementation Guidelines\n",
            "- " + "\n- ".join(security_analysis.suggestions[:5]) + "\n",
            "### Threat Awareness\n",
            "- " + "\n- ".join(threat_analysis.suggestions[:5]) + "\n",
            "### Historical Lessons\n",
            "- " + "\n- ".join(historical_analysis.suggestions[:5]) + "\n",
            "## Chapter Summary\n",
            f"This chapter has examined {topic} through the lens of history, security, and threat intelligence. ",
            "The convergence of these perspectives provides the foundation for effective cybersecurity practices.",
        ]

        return "\n".join(content_parts)

    def _generate_summary(self, content: str) -> str:
        """Generate a summary of the content."""
        # Simple extractive summary - in production, could use a summarization model
        sentences = content.split(". ")
        # Take first few sentences from each major section
        summary_sentences = []
        for sentence in sentences[:10]:  # Limit to avoid too long summaries
            if len(sentence) > 50 and any(
                word in sentence.lower()
                for word in ["cybersecurity", "security", "threat", "historical"]
            ):
                summary_sentences.append(sentence.strip())

        return ". ".join(summary_sentences[:3]) + "."

    def _extract_tags(self, topic: str, content: str) -> List[str]:
        """Extract relevant tags from topic and content."""
        base_tags = ["cybersecurity", "security"]

        # Add topic-specific tags
        topic_lower = topic.lower()
        if "ransomware" in topic_lower:
            base_tags.extend(["ransomware", "malware", "encryption"])
        if "phishing" in topic_lower:
            base_tags.extend(["phishing", "social_engineering", "email_security"])
        if "apt" in topic_lower or "advanced" in topic_lower:
            base_tags.extend(["apt", "threat_intelligence", "attribution"])

        # Add historical tags if historical content is significant
        if "historical" in content.lower() or "history" in content.lower():
            base_tags.append("historical_analysis")

        return list(set(base_tags))

    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content."""
        # Simple keyword extraction - could be enhanced with NLP
        key_terms = [
            "encryption",
            "authentication",
            "authorization",
            "threat_intelligence",
            "malware",
            "phishing",
            "social_engineering",
            "incident_response",
            "risk_management",
            "vulnerability",
            "exploit",
            "zero_day",
        ]

        found_concepts = []
        content_lower = content.lower()
        for term in key_terms:
            if term.replace("_", " ") in content_lower or term in content_lower:
                found_concepts.append(term.replace("_", " ").title())

        return found_concepts[:10]  # Limit to top 10

    def _generate_exercises(self, topic: str, learning_objectives: List[str]) -> List[str]:
        """Generate practice exercises for the topic."""
        exercises = [
            f"Research and document three real-world examples of {topic} incidents from the past five years.",
            f"Create a threat model for a hypothetical organization vulnerable to {topic}.",
            f"Design a detection strategy for identifying {topic} in your environment.",
            "Compare historical and modern approaches to similar security challenges.",
            "Develop an incident response plan specifically addressing this threat type.",
        ]

        # Add objective-specific exercises
        for obj in learning_objectives:
            if "analyze" in obj.lower():
                exercises.append(
                    f"Conduct a detailed analysis of how {topic} impacts different industry sectors."
                )
            elif "implement" in obj.lower():
                exercises.append(
                    f"Create an implementation checklist for deploying defenses against {topic}."
                )

        return exercises[:8]  # Limit number of exercises

    def _save_blog_post(self, blog_post: BlogPost):
        """Save blog post to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blog_post_{timestamp}.json"
        filepath = self.output_dir / filename

        with open(filepath, "w") as f:
            json.dump(blog_post.__dict__, f, indent=2)

    def _save_book_chapter(self, chapter: BookChapter):
        """Save book chapter to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chapter_{chapter.chapter_number}_{timestamp}.json"
        filepath = self.output_dir / filename

        with open(filepath, "w") as f:
            json.dump(chapter.__dict__, f, indent=2)

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and configuration information."""
        status = {
            "agents": {
                "security_analyst": (
                    "initialized" if hasattr(self, "security_analyst") else "failed"
                ),
                "threat_researcher": (
                    "initialized" if hasattr(self, "threat_researcher") else "failed"
                ),
                "historian": "initialized" if hasattr(self, "historian") else "failed",
            },
            "retrieval": {
                "web_search": "initialized" if self.web_retrieval else "failed",
                "threat_intel": "initialized" if self.threat_intel_rm else "failed",
                "historical": "initialized" if self.historical_rm else "failed",
            },
            "configuration": self.config.to_dict(),
            "output_directory": str(self.output_dir),
        }

        return status

    def _synthesize_basic_report(
        self,
        topic: str,
        security_analysis: AgentResponse,
        threat_analysis: AgentResponse,
        historical_analysis: AgentResponse,
    ) -> str:
        """Synthesize a basic research report when templates are not available."""

        content_parts = [
            f"# Cybersecurity Analysis: {topic}\n",
            "## Executive Summary\n",
            f"This report provides comprehensive analysis of {topic} from multiple cybersecurity perspectives.\n",
            "## Historical Context\n",
            historical_analysis.content + "\n",
            "## Security Analysis\n",
            security_analysis.content + "\n",
            "## Threat Intelligence\n",
            threat_analysis.content + "\n",
            "## Key Findings\n",
            "### Security Findings\n",
            "- " + "\n- ".join(security_analysis.suggestions[:3]) + "\n",
            "### Threat Findings\n",
            "- " + "\n- ".join(threat_analysis.suggestions[:3]) + "\n",
            "### Historical Insights\n",
            "- " + "\n- ".join(historical_analysis.suggestions[:3]) + "\n",
            "## Recommendations\n",
            "Based on our analysis, we recommend the following actions:\n",
            "1. "
            + "\n2. ".join((security_analysis.suggestions + threat_analysis.suggestions)[:5])
            + "\n",
            "## Conclusion\n",
            f"The analysis of {topic} reveals important implications for cybersecurity strategy and implementation. ",
            "Organizations should prioritize the recommended actions based on their risk tolerance and operational requirements.",
        ]

        return "\n".join(content_parts)

    def _save_research_report(self, report_data: Dict[str, Any]):
        """Save research report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_type = report_data["metadata"].get("report_type", "analysis")
        filename = f"research_report_{report_type}_{timestamp}.json"
        filepath = self.output_dir / filename

        with open(filepath, "w") as f:
            json.dump(report_data, f, indent=2)
