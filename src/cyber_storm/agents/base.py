"""
Base agent class for Cyber-Researcher agents.

This module provides the foundation for specialized agents that participate
in Co-STORM collaborative discourse for cybersecurity narrative generation.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from dataclasses import dataclass

from knowledge_storm.lm import LM
from dspy.retrieve import Retrieve


class AgentRole(Enum):
    """Enumeration of available agent roles."""

    SECURITY_ANALYST = "security_analyst"
    THREAT_RESEARCHER = "threat_researcher"
    HISTORIAN = "historian"
    MODERATOR = "moderator"


class ContentType(Enum):
    """Types of content the agent can generate."""

    BLOG_POST = "blog_post"
    BOOK_CHAPTER = "book_chapter"
    RESEARCH_REPORT = "research_report"
    NARRATIVE_OUTLINE = "narrative_outline"


@dataclass
class AgentContext:
    """Context information for agent operations."""

    topic: str
    content_type: ContentType
    target_audience: str = "cybersecurity professionals"
    technical_depth: str = "intermediate"
    narrative_style: str = "educational"
    historical_focus: bool = True
    max_sources: int = 10


@dataclass
class AgentResponse:
    """Structured response from an agent."""

    content: str
    sources: List[str]
    confidence: float
    suggestions: List[str]
    metadata: Dict[str, Any]


class BaseCyberAgent(ABC):
    """
    Abstract base class for all Cyber-Researcher agents.

    This class provides the common interface and functionality that all
    specialized agents (Security Analyst, Threat Researcher, Historian)
    must implement.
    """

    def __init__(
        self,
        role: AgentRole,
        language_model: LM,
        retrieval_module: Optional[Retrieve] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the base agent.

        Args:
            role: The specific role this agent plays
            language_model: The LM to use for generation
            retrieval_module: Optional RM for information retrieval
            config: Optional configuration parameters
        """
        self.role = role
        self.language_model = language_model
        self.retrieval_module = retrieval_module
        self.config = config or {}

        # Agent-specific configuration
        self.perspective = self._get_perspective()
        self.expertise_areas = self._get_expertise_areas()
        self.response_style = self._get_response_style()

    @abstractmethod
    def _get_perspective(self) -> str:
        """Return the unique perspective this agent brings to discussions."""
        pass

    @abstractmethod
    def _get_expertise_areas(self) -> List[str]:
        """Return the areas of expertise for this agent."""
        pass

    @abstractmethod
    def _get_response_style(self) -> Dict[str, Any]:
        """Return the preferred response style for this agent."""
        pass

    @abstractmethod
    def analyze_topic(self, context: AgentContext) -> AgentResponse:
        """
        Analyze a given topic from this agent's perspective.

        Args:
            context: The context for analysis

        Returns:
            AgentResponse with analysis and insights
        """
        pass

    @abstractmethod
    def generate_questions(self, context: AgentContext) -> List[str]:
        """
        Generate relevant questions about a topic.

        Args:
            context: The context for question generation

        Returns:
            List of questions from this agent's perspective
        """
        pass

    @abstractmethod
    def review_content(self, content: str, context: AgentContext) -> AgentResponse:
        """
        Review and provide feedback on generated content.

        Args:
            content: The content to review
            context: The context for review

        Returns:
            AgentResponse with feedback and suggestions
        """
        pass

    def retrieve_information(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve information using the configured retrieval module.

        Args:
            query: The search query
            max_results: Maximum number of results to return

        Returns:
            List of retrieved information items
        """
        if not self.retrieval_module:
            return []

        try:
            # Check if it's a custom retrieval module with retrieve method
            if hasattr(self.retrieval_module, "retrieve") and callable(
                getattr(self.retrieval_module, "retrieve")
            ):
                results = self.retrieval_module.retrieve(query, k=max_results)
            else:
                # For SerperRM and other knowledge_storm RMs, use __call__
                # Note: k parameter is set during initialization, not at runtime
                results = self.retrieval_module(query)

            # Handle different result formats
            formatted_results = []
            for r in results:
                if hasattr(r, "raw_utterance"):
                    content = r.raw_utterance
                elif hasattr(r, "snippet"):
                    content = r.snippet
                elif hasattr(r, "snippets"):
                    content = r.snippets
                else:
                    content = str(r)

                formatted_results.append(
                    {
                        "content": content,
                        "url": getattr(r, "url", ""),
                        "title": getattr(r, "title", ""),
                    }
                )

            return formatted_results
        except Exception as e:
            print(f"Retrieval error for {self.role.value}: {e}")
            return []

    def _format_prompt(self, template: str, **kwargs) -> str:
        """
        Format a prompt template with the given parameters.

        Args:
            template: The prompt template
            **kwargs: Parameters to substitute in the template

        Returns:
            Formatted prompt string
        """
        # Add agent-specific context
        agent_context = {
            "role": self.role.value,
            "perspective": self.perspective,
            "expertise": ", ".join(self.expertise_areas),
        }

        return template.format(**agent_context, **kwargs)

    def _generate_response(self, prompt: str) -> str:
        """
        Generate a response using the language model.

        Args:
            prompt: The input prompt

        Returns:
            Generated response text
        """
        try:
            # Language models in knowledge_storm use __call__ method
            response = self.language_model(
                prompt,
                temperature=self.config.get("temperature", 0.8),
                max_tokens=self.config.get("max_tokens", 1000),
            )
            # Handle response content
            if hasattr(response, "content"):
                content = response.content
                # If content is a list, join it or take the first element
                if isinstance(content, list):
                    if len(content) == 1:
                        return content[0]
                    else:
                        return "\n".join(str(item) for item in content)
                return str(content)
            else:
                result = str(response)
                # If the string representation looks like a list, try to parse it
                if result.startswith("['") and result.endswith("']"):
                    try:
                        import ast

                        parsed = ast.literal_eval(result)
                        if isinstance(parsed, list) and len(parsed) == 1:
                            return parsed[0]
                        elif isinstance(parsed, list):
                            return "\n".join(str(item) for item in parsed)
                    except (ValueError, SyntaxError):
                        pass
                return result
        except Exception as e:
            print(f"Generation error for {self.role.value}: {e}")
            return f"Error generating response: {e}"

    def get_agent_description(self) -> str:
        """Return a description of this agent for Co-STORM integration."""
        return f"""
Role: {self.role.value.replace('_', ' ').title()}
Perspective: {self.perspective}
Expertise: {', '.join(self.expertise_areas)}
Focus: Brings {self.perspective} to cybersecurity topics with historical context
"""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.role.value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(role={self.role}, lm={self.language_model})"
