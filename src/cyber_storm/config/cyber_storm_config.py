"""
Configuration management for Cyber-Researcher.

This module provides configuration classes and utilities for managing
the various settings and parameters of the Cyber-Researcher system.
"""

import os
import toml
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path

from knowledge_storm.lm import ClaudeModel


@dataclass
class LMConfig:
    """Configuration for language models."""

    model_name: str
    max_tokens: int = 1000
    temperature: float = 0.8
    top_p: float = 0.9
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    api_version: Optional[str] = None


@dataclass
class AgentConfig:
    """Configuration for individual agents."""

    enabled: bool = True
    lm_config: LMConfig = field(default_factory=lambda: LMConfig("gpt-3.5-turbo"))
    custom_instructions: str = ""
    expertise_focus: List[str] = field(default_factory=list)


@dataclass
class RetrievalConfig:
    """Configuration for retrieval modules."""

    search_engine: str = "serper"  # serper, bing, you, brave, duckduckgo, etc.
    vector_store_type: str = "local"  # local, cloud
    vector_store_path: str = "./vector_store"
    embedding_model: str = "BAAI/bge-m3"
    device: str = "cpu"
    max_results_per_query: int = 10
    qdrant_url: Optional[str] = None
    qdrant_api_key: Optional[str] = None


@dataclass
class GenerationConfig:
    """Configuration for content generation."""

    default_content_type: str = "blog_post"
    default_audience: str = "cybersecurity professionals"
    default_technical_depth: str = "intermediate"
    default_narrative_style: str = "educational"
    include_historical_context: bool = True
    max_conversation_turns: int = 3
    max_perspectives: int = 3


@dataclass
class OutputConfig:
    """Configuration for output formatting and saving."""

    output_directory: str = "./output"
    save_conversation_logs: bool = True
    save_intermediate_results: bool = True
    include_citations: bool = True
    citation_format: str = "markdown"  # markdown, academic, chicago


class CyberStormConfig:
    """
    Main configuration class for Cyber-Researcher.

    This class manages all configuration aspects of the system and provides
    methods for loading from files and environment variables.
    """

    def __init__(
        self,
        config_file: Optional[Union[str, Path]] = None,
        secrets_file: Optional[Union[str, Path]] = None,
    ):
        """
        Initialize configuration.

        Args:
            config_file: Path to main configuration file
            secrets_file: Path to secrets file (default: secrets.toml)
        """
        self.config_file = Path(config_file) if config_file else None
        self.secrets_file = Path(secrets_file) if secrets_file else Path("secrets.toml")

        # Load configuration
        self._load_secrets()
        self._load_config()
        self._setup_default_configs()

    def _load_secrets(self):
        """Load API keys and secrets from file."""
        self.secrets = {}

        if self.secrets_file.exists():
            try:
                self.secrets = toml.load(self.secrets_file)
            except Exception as e:
                print(f"Error loading secrets file: {e}")

        # Override with environment variables
        env_vars = [
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "OPENAI_API_TYPE",
            "AZURE_API_BASE",
            "AZURE_API_VERSION",
            "BING_SEARCH_API_KEY",
            "YOU_API_KEY",
            "SERPER_API_KEY",
            "BRAVE_API_KEY",
            "TAVILY_API_KEY",
            "QDRANT_API_KEY",
            "QDRANT_URL",
            "HUGGINGFACE_API_KEY",
        ]

        for var in env_vars:
            if os.getenv(var):
                self.secrets[var] = os.getenv(var)

    def _load_config(self):
        """Load main configuration from file."""
        self.config_data = {}

        if self.config_file and self.config_file.exists():
            try:
                self.config_data = toml.load(self.config_file)
            except Exception as e:
                print(f"Error loading config file: {e}")

    def _setup_default_configs(self):
        """Set up default configuration objects."""
        # Language model configurations - Claude as default
        claude_kwargs = {
            "api_key": self.secrets.get("ANTHROPIC_API_KEY"),
            "temperature": 0.8,
            "top_p": 0.9,
        }

        # Agent configurations using Claude models
        self.security_analyst_config = AgentConfig(
            lm_config=LMConfig(
                model_name=self.secrets.get("DEFAULT_GENERATION_MODEL", "claude-3-sonnet-20240229"),
                max_tokens=1000,
                **claude_kwargs,
            ),
            custom_instructions="Focus on defensive security and technical accuracy.",
            expertise_focus=["network_security", "endpoint_protection", "incident_response"],
        )

        self.threat_researcher_config = AgentConfig(
            lm_config=LMConfig(
                model_name=self.secrets.get("DEFAULT_GENERATION_MODEL", "claude-3-sonnet-20240229"),
                max_tokens=1000,
                **claude_kwargs,
            ),
            custom_instructions="Focus on threat intelligence and adversary analysis.",
            expertise_focus=["threat_intelligence", "malware_analysis", "attribution"],
        )

        self.historian_config = AgentConfig(
            lm_config=LMConfig(
                model_name=self.secrets.get("DEFAULT_ARTICLE_MODEL", "claude-3-opus-20240229"),
                max_tokens=1000,
                **claude_kwargs,
            ),
            custom_instructions="Focus on historical context and narrative generation.",
            expertise_focus=["historical_analysis", "storytelling", "educational_content"],
        )

        # Retrieval configuration using Hugging Face embeddings by default
        self.retrieval_config = RetrievalConfig(
            search_engine="serper",
            vector_store_path="./vector_store",
            embedding_model=self.secrets.get("DEFAULT_EMBEDDING_MODEL", "BAAI/bge-m3"),
            device="cpu",
            qdrant_url=self.secrets.get("QDRANT_URL"),
            qdrant_api_key=self.secrets.get("QDRANT_API_KEY"),
        )

        # Generation configuration
        self.generation_config = GenerationConfig(
            default_content_type="blog_post",
            default_audience="cybersecurity professionals",
            include_historical_context=True,
        )

        # Output configuration
        self.output_config = OutputConfig(
            output_directory="./output", save_conversation_logs=True, include_citations=True
        )

    def get_lm_for_agent(self, agent_type: str) -> ClaudeModel:
        """
        Get a configured language model for a specific agent.

        Args:
            agent_type: Type of agent ("security_analyst", "threat_researcher", "historian")

        Returns:
            Configured ClaudeModel instance
        """
        config_map = {
            "security_analyst": self.security_analyst_config,
            "threat_researcher": self.threat_researcher_config,
            "historian": self.historian_config,
        }

        agent_config = config_map.get(agent_type)
        if not agent_config:
            raise ValueError(f"Unknown agent type: {agent_type}")

        lm_config = agent_config.lm_config

        return ClaudeModel(
            model=lm_config.model_name,
            max_tokens=lm_config.max_tokens,
            temperature=lm_config.temperature,
            top_p=lm_config.top_p,
            api_key=lm_config.api_key,
        )

    def get_search_api_key(self, search_engine: str) -> Optional[str]:
        """
        Get API key for a specific search engine.

        Args:
            search_engine: Name of the search engine

        Returns:
            API key or None if not found
        """
        key_map = {
            "bing": "BING_SEARCH_API_KEY",
            "you": "YOU_API_KEY",
            "serper": "SERPER_API_KEY",
            "brave": "BRAVE_API_KEY",
            "tavily": "TAVILY_API_KEY",
        }

        key_name = key_map.get(search_engine)
        return self.secrets.get(key_name) if key_name else None

    def validate_config(self) -> List[str]:
        """
        Validate configuration and return list of issues.

        Returns:
            List of validation error messages
        """
        issues = []

        # Check required API keys - Claude is now primary
        if not self.secrets.get("ANTHROPIC_API_KEY"):
            issues.append("Missing ANTHROPIC_API_KEY")

        # Check search engine configuration
        search_engine = self.retrieval_config.search_engine
        if search_engine != "duckduckgo" and not self.get_search_api_key(search_engine):
            issues.append(f"Missing API key for search engine: {search_engine}")

        # Check vector store configuration
        if self.retrieval_config.vector_store_type == "cloud":
            if not self.secrets.get("QDRANT_URL"):
                issues.append("Missing QDRANT_URL for cloud vector store")
            if not self.secrets.get("QDRANT_API_KEY"):
                issues.append("Missing QDRANT_API_KEY for cloud vector store")

        # Check output directory
        output_dir = Path(self.output_config.output_directory)
        if not output_dir.exists():
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create output directory: {e}")

        return issues

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "security_analyst": {
                "enabled": self.security_analyst_config.enabled,
                "model": self.security_analyst_config.lm_config.model_name,
                "expertise_focus": self.security_analyst_config.expertise_focus,
            },
            "threat_researcher": {
                "enabled": self.threat_researcher_config.enabled,
                "model": self.threat_researcher_config.lm_config.model_name,
                "expertise_focus": self.threat_researcher_config.expertise_focus,
            },
            "historian": {
                "enabled": self.historian_config.enabled,
                "model": self.historian_config.lm_config.model_name,
                "expertise_focus": self.historian_config.expertise_focus,
            },
            "retrieval": {
                "search_engine": self.retrieval_config.search_engine,
                "vector_store_type": self.retrieval_config.vector_store_type,
                "embedding_model": self.retrieval_config.embedding_model,
            },
            "generation": {
                "default_content_type": self.generation_config.default_content_type,
                "default_audience": self.generation_config.default_audience,
                "include_historical_context": self.generation_config.include_historical_context,
            },
        }

    def save_config(self, output_path: Union[str, Path]):
        """
        Save current configuration to file.

        Args:
            output_path: Path to save configuration
        """
        config_dict = self.to_dict()

        with open(output_path, "w") as f:
            toml.dump(config_dict, f)

    @classmethod
    def create_default_config(cls, output_path: Union[str, Path]):
        """
        Create a default configuration file.

        Args:
            output_path: Path to save the default configuration
        """
        default_config = {
            "security_analyst": {
                "enabled": True,
                "model": "claude-3-sonnet-20240229",
                "expertise_focus": ["network_security", "endpoint_protection", "incident_response"],
            },
            "threat_researcher": {
                "enabled": True,
                "model": "claude-3-sonnet-20240229",
                "expertise_focus": ["threat_intelligence", "malware_analysis", "attribution"],
            },
            "historian": {
                "enabled": True,
                "model": "claude-3-opus-20240229",
                "expertise_focus": ["historical_analysis", "storytelling", "educational_content"],
            },
            "retrieval": {
                "search_engine": "serper",
                "vector_store_type": "local",
                "embedding_model": "BAAI/bge-m3",
                "device": "cpu",
                "max_results_per_query": 10,
            },
            "generation": {
                "default_content_type": "blog_post",
                "default_audience": "cybersecurity professionals",
                "default_technical_depth": "intermediate",
                "include_historical_context": True,
                "max_conversation_turns": 3,
            },
            "output": {
                "output_directory": "./output",
                "save_conversation_logs": True,
                "include_citations": True,
                "citation_format": "markdown",
            },
        }

        with open(output_path, "w") as f:
            toml.dump(default_config, f)
