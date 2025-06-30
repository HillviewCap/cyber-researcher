"""
Cyber-Researcher Retrieval Module

This module contains specialized retrieval modules for cybersecurity narrative generation:
- ThreatIntelRM: Retrieval for threat intelligence reports and cybersecurity content
- HistoricalRM: Retrieval for historical events and context relevant to cybersecurity
"""

from .threat_intel_rm import ThreatIntelRM, ThreatIntelReport
from .historical_rm import HistoricalRM, HistoricalEvent

__all__ = ["ThreatIntelRM", "ThreatIntelReport", "HistoricalRM", "HistoricalEvent"]
