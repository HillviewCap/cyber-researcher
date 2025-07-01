"""
Unit tests for Cyber-Researcher agents.

Tests the functionality of SecurityAnalystAgent, ThreatResearcherAgent,
and HistorianAgent classes.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cyber_storm.agents import (
    SecurityAnalystAgent,
    ThreatResearcherAgent,
    HistorianAgent,
    AgentContext,
    ContentType,
    AgentRole,
)
from knowledge_storm.interface import Information


class TestSecurityAnalystAgent:
    """Test cases for SecurityAnalystAgent."""

    @pytest.fixture
    def mock_lm(self):
        """Create a mock language model."""
        lm = Mock()
        lm.generate.return_value = "Mock security analysis response"
        return lm

    @pytest.fixture
    def security_agent(self, mock_lm):
        """Create SecurityAnalystAgent instance with mock LM."""
        config = {"model": "mock-model", "temperature": 0.7}
        agent = SecurityAnalystAgent(language_model=mock_lm, config=config)
        agent.retrieval_module = Mock()
        # Return proper Information objects
        test_info = Information(
            url="http://test.com",
            title="Test Security Report",
            snippets="Security content for testing",
            description="Mock security report for testing",
        )
        agent.retrieval_module.retrieve.return_value = [test_info]
        return agent

    def test_agent_initialization(self, security_agent):
        """Test agent initialization."""
        assert security_agent.role == AgentRole.SECURITY_ANALYST
        assert "Network Security" in security_agent.expertise_areas
        assert security_agent.perspective == "defensive security and technical analysis"

    def test_analyze_topic(self, security_agent):
        """Test topic analysis functionality."""
        context = AgentContext(
            topic="Ransomware Defense Strategies",
            content_type=ContentType.BLOG_POST,
            target_audience="security professionals",
            technical_depth="intermediate",
        )

        response = security_agent.analyze_topic(context)

        assert response.content is not None
        assert len(response.sources) > 0
        assert response.confidence > 0
        assert len(response.suggestions) > 0
        assert response.metadata["agent_role"] == "security_analyst"

    def test_generate_questions(self, security_agent):
        """Test question generation functionality."""
        context = AgentContext(
            topic="Zero Trust Architecture", content_type=ContentType.RESEARCH_REPORT
        )

        questions = security_agent.generate_questions(context)

        assert isinstance(questions, list)
        assert len(questions) <= 10
        # Should generate relevant security questions
        assert any("security" in q.lower() or "defense" in q.lower() for q in questions)

    def test_review_content(self, security_agent):
        """Test content review functionality."""
        content = "This is test cybersecurity content about network security."
        context = AgentContext(topic="Network Security", target_audience="beginners")

        review = security_agent.review_content(content, context)

        assert review.content is not None
        assert review.confidence > 0
        assert len(review.suggestions) > 0

    def test_get_security_controls_for_topic(self, security_agent):
        """Test security controls mapping."""
        ransomware_controls = security_agent.get_security_controls_for_topic("ransomware attack")
        assert "Backup and Recovery" in ransomware_controls
        assert "Endpoint Detection and Response" in ransomware_controls

        phishing_controls = security_agent.get_security_controls_for_topic("phishing campaign")
        assert "Email Filtering" in phishing_controls
        assert "User Awareness Training" in phishing_controls

        # Test default controls for unknown topic
        unknown_controls = security_agent.get_security_controls_for_topic("unknown threat")
        assert "Access Controls" in unknown_controls


class TestThreatResearcherAgent:
    """Test cases for ThreatResearcherAgent."""

    @pytest.fixture
    def mock_lm(self):
        """Create a mock language model."""
        lm = Mock()
        lm.generate.return_value = "Mock threat intelligence response"
        return lm

    @pytest.fixture
    def threat_agent(self, mock_lm):
        """Create ThreatResearcherAgent instance with mock LM."""
        config = {"model": "mock-model", "temperature": 0.8}
        agent = ThreatResearcherAgent(language_model=mock_lm, config=config)
        agent.retrieval_module = Mock()
        # Return proper Information objects
        test_info = Information(
            url="http://threat.com",
            title="Threat Intel Report",
            snippets="Threat intelligence content for testing",
            description="Mock threat intelligence report for testing",
        )
        agent.retrieval_module.retrieve.return_value = [test_info]
        return agent

    def test_agent_initialization(self, threat_agent):
        """Test agent initialization."""
        assert threat_agent.role == AgentRole.THREAT_RESEARCHER
        assert "Threat Intelligence" in threat_agent.expertise_areas
        assert threat_agent.perspective == "threat intelligence and adversary analysis"

    def test_analyze_topic(self, threat_agent):
        """Test threat analysis functionality."""
        context = AgentContext(
            topic="APT29 Campaign Analysis",
            content_type=ContentType.RESEARCH_REPORT,
            technical_depth="advanced",
        )

        response = threat_agent.analyze_topic(context)

        assert response.content is not None
        assert response.metadata["agent_role"] == "threat_researcher"
        assert response.metadata["analysis_type"] == "threat_intelligence"

    def test_analyze_threat_actor(self, threat_agent):
        """Test threat actor analysis."""
        actor_profile = threat_agent.analyze_threat_actor("APT29")

        assert isinstance(actor_profile, dict)
        assert "attribution" in actor_profile
        assert "techniques" in actor_profile
        assert "targets" in actor_profile

    def test_get_mitre_techniques(self, threat_agent):
        """Test MITRE ATT&CK technique mapping."""
        techniques = threat_agent.get_mitre_techniques_for_threat("spearphishing")

        assert isinstance(techniques, list)
        assert any("T1566" in tech for tech in techniques)  # Phishing technique

    def test_assess_threat_severity(self, threat_agent):
        """Test threat severity assessment."""
        severity = threat_agent.assess_threat_severity("ransomware", "financial")

        assert severity in ["low", "medium", "high", "critical"]


class TestHistorianAgent:
    """Test cases for HistorianAgent."""

    @pytest.fixture
    def mock_lm(self):
        """Create a mock language model."""
        lm = Mock()
        lm.generate.return_value = "Mock historical narrative response"
        return lm

    @pytest.fixture
    def historian_agent(self, mock_lm):
        """Create HistorianAgent instance with mock LM."""
        config = {"model": "mock-model", "temperature": 0.9}
        agent = HistorianAgent(language_model=mock_lm, config=config)
        agent.retrieval_module = Mock()
        # Return proper Information objects
        test_info = Information(
            url="http://history.com",
            title="Historical Event",
            snippets="Historical content for testing",
            description="Mock historical event for testing",
        )
        agent.retrieval_module.retrieve.return_value = [test_info]
        return agent

    def test_agent_initialization(self, historian_agent):
        """Test agent initialization."""
        assert historian_agent.role == AgentRole.HISTORIAN
        assert "Military History" in historian_agent.expertise_areas
        assert historian_agent.perspective == "historical context and narrative storytelling"

    def test_analyze_topic(self, historian_agent):
        """Test historical analysis functionality."""
        context = AgentContext(
            topic="Cyber Warfare Evolution",
            content_type=ContentType.BOOK_CHAPTER,
            historical_focus=True,
        )

        response = historian_agent.analyze_topic(context)

        assert response.content is not None
        assert response.metadata["agent_role"] == "historian"
        assert response.metadata["analysis_type"] == "historical_narrative"

    def test_find_historical_parallels(self, historian_agent):
        """Test historical parallel finding."""
        parallels = historian_agent.find_historical_parallels("social engineering")

        assert isinstance(parallels, list)
        assert len(parallels) > 0
        assert any("trojan horse" in p.lower() for p in parallels)

    def test_create_narrative_framework(self, historian_agent):
        """Test narrative framework creation."""
        framework = historian_agent.create_narrative_framework("encryption", "ancient codes")

        assert isinstance(framework, dict)
        assert "introduction" in framework
        assert "historical_context" in framework
        assert "modern_parallel" in framework
        assert "conclusion" in framework

    def test_get_historical_periods(self, historian_agent):
        """Test historical period mapping."""
        periods = historian_agent.get_relevant_historical_periods("cryptography")

        assert isinstance(periods, list)
        assert any("world war" in period.lower() for period in periods)


class TestAgentContext:
    """Test cases for AgentContext dataclass."""

    def test_agent_context_creation(self):
        """Test AgentContext creation with various parameters."""
        context = AgentContext(
            topic="Test Topic",
            content_type=ContentType.BLOG_POST,
            target_audience="professionals",
            technical_depth="intermediate",
            narrative_style="educational",
            historical_focus=True,
            max_sources=5,
        )

        assert context.topic == "Test Topic"
        assert context.content_type == ContentType.BLOG_POST
        assert context.target_audience == "professionals"
        assert context.technical_depth == "intermediate"
        assert context.narrative_style == "educational"
        assert context.historical_focus is True
        assert context.max_sources == 5

    def test_agent_context_defaults(self):
        """Test AgentContext with default values."""
        context = AgentContext(topic="Test")

        assert context.content_type == ContentType.BLOG_POST
        assert context.target_audience == "general"
        assert context.technical_depth == "intermediate"
        assert context.narrative_style == "educational"
        assert context.historical_focus is False
        assert context.max_sources == 10


# Integration tests for agent interactions
class TestAgentIntegration:
    """Integration tests for agent collaboration."""

    @pytest.fixture
    def mock_agents(self):
        """Create mock instances of all agents."""
        mock_lm = Mock()
        mock_lm.generate.return_value = "Mock response"

        config = {"model": "mock", "temperature": 0.7}

        security = SecurityAnalystAgent(language_model=mock_lm, config=config)
        threat = ThreatResearcherAgent(language_model=mock_lm, config=config)
        historian = HistorianAgent(language_model=mock_lm, config=config)

        # Mock retrieval modules
        for agent in [security, threat, historian]:
            agent.retrieval_module = Mock()
            agent.retrieval_module.retrieve.return_value = [
                {"title": "Test", "content": "Test content", "url": "http://test.com"}
            ]

        return security, threat, historian

    def test_multi_agent_analysis(self, mock_agents):
        """Test coordinated analysis from multiple agents."""
        security, threat, historian = mock_agents

        context = AgentContext(
            topic="Advanced Persistent Threats", content_type=ContentType.RESEARCH_REPORT
        )

        # Get analysis from all agents
        security_analysis = security.analyze_topic(context)
        threat_analysis = threat.analyze_topic(context)
        historical_analysis = historian.analyze_topic(context)

        # Verify all agents provide responses
        assert security_analysis.content is not None
        assert threat_analysis.content is not None
        assert historical_analysis.content is not None

        # Verify different perspectives
        assert security_analysis.metadata["agent_role"] == "security_analyst"
        assert threat_analysis.metadata["agent_role"] == "threat_researcher"
        assert historical_analysis.metadata["agent_role"] == "historian"

    def test_agent_specialization(self, mock_agents):
        """Test that agents provide specialized perspectives."""
        security, threat, historian = mock_agents

        # Security agent should focus on defense
        assert "defensive" in security.perspective.lower()
        assert any("defense" in area.lower() for area in security.expertise_areas)

        # Threat agent should focus on adversaries
        assert "threat" in threat.perspective.lower()
        assert any("threat" in area.lower() for area in threat.expertise_areas)

        # Historian should focus on context
        assert "historical" in historian.perspective.lower()
        assert any("history" in area.lower() for area in historian.expertise_areas)
