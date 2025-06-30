"""
Cyber-Researcher Agent Module

This module contains specialized agents for cybersecurity narrative generation:
- SecurityAnalystAgent: Focuses on defensive security and technical analysis
- ThreatResearcherAgent: Specializes in threat intelligence and adversary analysis
- HistorianAgent: Provides historical context and narrative frameworks
"""

from .base import BaseCyberAgent, AgentRole, AgentContext, AgentResponse, ContentType
from .security_analyst import SecurityAnalystAgent
from .threat_researcher import ThreatResearcherAgent
from .historian import HistorianAgent

__all__ = [
    "BaseCyberAgent",
    "AgentRole",
    "AgentContext",
    "AgentResponse",
    "ContentType",
    "SecurityAnalystAgent",
    "ThreatResearcherAgent",
    "HistorianAgent",
]
