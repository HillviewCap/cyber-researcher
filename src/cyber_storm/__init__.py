"""
Cyber-Researcher: A narrative-focused cybersecurity research assistant.

This package provides tools for generating educational cybersecurity content
by blending historical narratives with technical concepts.
"""

__version__ = "0.1.0"

from .runner import CyberStormRunner, BlogPost, BookChapter, InteractiveSession
from .config import CyberStormConfig
from .agents import SecurityAnalystAgent, ThreatResearcherAgent, HistorianAgent

__all__ = [
    "CyberStormRunner",
    "BlogPost",
    "BookChapter",
    "InteractiveSession",
    "CyberStormConfig",
    "SecurityAnalystAgent",
    "ThreatResearcherAgent",
    "HistorianAgent",
]
