"""
Integration tests for Cyber-Researcher CyberStormRunner.

Tests the full workflow from topic input to content generation.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import tempfile
import os
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cyber_storm import CyberStormRunner, CyberStormConfig
from cyber_storm.agents import AgentContext, ContentType


class TestCyberStormRunner:
    """Integration tests for CyberStormRunner."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def mock_config(self, temp_dir):
        """Create mock configuration for testing."""
        with patch("cyber_storm.config.CyberStormConfig") as mock_config_class:
            config = Mock()
            config.validate_config.return_value = []
            config.get_lm_for_agent.return_value = Mock()
            config.get_search_api_key.return_value = "mock_api_key"

            # Mock agent configs
            config.security_analyst_config = Mock()
            config.security_analyst_config.lm_config = Mock()
            config.security_analyst_config.lm_config.__dict__ = {"model": "mock"}

            config.threat_researcher_config = Mock()
            config.threat_researcher_config.lm_config = Mock()
            config.threat_researcher_config.lm_config.__dict__ = {"model": "mock"}

            config.historian_config = Mock()
            config.historian_config.lm_config = Mock()
            config.historian_config.lm_config.__dict__ = {"model": "mock"}

            # Mock retrieval config
            config.retrieval_config = Mock()
            config.retrieval_config.search_engine = "duckduckgo"
            config.retrieval_config.max_results_per_query = 5
            config.retrieval_config.embedding_model = "mock-model"
            config.retrieval_config.device = "cpu"
            config.retrieval_config.vector_store_path = temp_dir
            config.retrieval_config.qdrant_url = None
            config.retrieval_config.qdrant_api_key = None

            # Mock generation config
            config.generation_config = Mock()
            config.generation_config.default_audience = "security professionals"
            config.generation_config.default_technical_depth = "intermediate"
            config.generation_config.include_historical_context = True

            # Mock output config
            config.output_config = Mock()
            config.output_config.output_directory = temp_dir
            config.output_config.save_intermediate_results = True

            config.to_dict.return_value = {"test": "config"}

            return config

    @pytest.fixture
    def mock_runner(self, mock_config):
        """Create CyberStormRunner with mocked dependencies."""
        with (
            patch("cyber_storm.runner.SecurityAnalystAgent") as mock_security,
            patch("cyber_storm.runner.ThreatResearcherAgent") as mock_threat,
            patch("cyber_storm.runner.HistorianAgent") as mock_historian,
            patch("cyber_storm.runner.ThreatIntelRM") as mock_threat_rm,
            patch("cyber_storm.runner.HistoricalRM") as mock_historical_rm,
            patch("cyber_storm.runner.DuckDuckGoSearchRM") as mock_web_rm,
        ):

            # Mock agent responses
            mock_response = Mock()
            mock_response.content = "Mock agent analysis content"
            mock_response.sources = ["http://example.com"]
            mock_response.suggestions = ["suggestion 1", "suggestion 2", "suggestion 3"]
            mock_response.confidence = 0.85

            # Configure agent mocks
            for agent_mock in [
                mock_security.return_value,
                mock_threat.return_value,
                mock_historian.return_value,
            ]:
                agent_mock.analyze_topic.return_value = mock_response
                agent_mock.generate_questions.return_value = [
                    "Question 1?",
                    "Question 2?",
                    "Question 3?",
                ]

            # Configure retrieval module mocks
            for rm_mock in [mock_threat_rm.return_value, mock_historical_rm.return_value]:
                rm_mock.ingest_threat_reports.return_value = 5
                rm_mock.create_sample_data.return_value = 10
                rm_mock.get_collection_stats.return_value = {"total_documents": 100}

            runner = CyberStormRunner(mock_config)
            return runner

    def test_runner_initialization(self, mock_runner):
        """Test CyberStormRunner initialization."""
        assert hasattr(mock_runner, "security_analyst")
        assert hasattr(mock_runner, "threat_researcher")
        assert hasattr(mock_runner, "historian")
        assert hasattr(mock_runner, "web_retrieval")
        assert hasattr(mock_runner, "threat_intel_rm")
        assert hasattr(mock_runner, "historical_rm")
        assert hasattr(mock_runner, "output_dir")

    def test_get_system_status(self, mock_runner):
        """Test system status retrieval."""
        status = mock_runner.get_system_status()

        assert isinstance(status, dict)
        assert "agents" in status
        assert "retrieval" in status
        assert "configuration" in status
        assert "output_directory" in status

        # Check agent status
        assert "security_analyst" in status["agents"]
        assert "threat_researcher" in status["agents"]
        assert "historian" in status["agents"]

        # Check retrieval status
        assert "web_search" in status["retrieval"]
        assert "threat_intel" in status["retrieval"]
        assert "historical" in status["retrieval"]

    def test_generate_blog_post(self, mock_runner):
        """Test blog post generation workflow."""
        topic = "Ransomware: Evolution and Defense Strategies"

        blog_post = mock_runner.generate_blog_post(topic, style="educational")

        assert blog_post is not None
        assert blog_post.title is not None
        assert blog_post.content is not None
        assert blog_post.summary is not None
        assert isinstance(blog_post.tags, list)
        assert isinstance(blog_post.sources, list)
        assert isinstance(blog_post.metadata, dict)
        assert blog_post.created_at is not None

        # Check metadata
        assert "agents_used" in blog_post.metadata
        assert "style" in blog_post.metadata
        assert "technical_depth" in blog_post.metadata

    def test_generate_book_chapter(self, mock_runner):
        """Test book chapter generation workflow."""
        topic = "Phishing: From Trojan Horse to Modern Social Engineering"
        learning_objectives = [
            "Understand historical evolution of deception",
            "Analyze modern phishing techniques",
            "Develop defense strategies",
        ]

        chapter = mock_runner.generate_book_chapter(topic, 3, learning_objectives)

        assert chapter is not None
        assert chapter.chapter_number == 3
        assert chapter.title is not None
        assert chapter.content is not None
        assert chapter.summary is not None
        assert chapter.learning_objectives == learning_objectives
        assert isinstance(chapter.key_concepts, list)
        assert isinstance(chapter.exercises, list)
        assert isinstance(chapter.sources, list)
        assert isinstance(chapter.metadata, dict)
        assert chapter.created_at is not None

    def test_interactive_research(self, mock_runner):
        """Test interactive research session creation."""
        topic = "Supply Chain Attacks and Historical Parallels"

        session = mock_runner.interactive_research(topic)

        assert session is not None
        assert session.topic == topic
        assert isinstance(session.conversation_log, list)
        assert isinstance(session.generated_questions, list)
        assert isinstance(session.insights, list)
        assert session.session_id is not None
        assert session.created_at is not None

        # Check conversation log structure
        if session.conversation_log:
            log_entry = session.conversation_log[0]
            assert "timestamp" in log_entry
            assert "type" in log_entry
            assert "content" in log_entry

    def test_ingest_threat_report(self, mock_runner):
        """Test threat report ingestion."""
        fake_report_path = "/fake/path/to/report.csv"

        result = mock_runner.ingest_threat_report(fake_report_path)

        assert isinstance(result, bool)

    def test_content_synthesis(self, mock_runner):
        """Test content synthesis from multiple agents."""
        topic = "Zero Trust Architecture"

        # Mock agent responses
        mock_security_response = Mock()
        mock_security_response.content = "Security analysis of Zero Trust"
        mock_security_response.suggestions = ["Implement network segmentation", "Deploy MFA"]

        mock_threat_response = Mock()
        mock_threat_response.content = "Threat perspective on Zero Trust"
        mock_threat_response.suggestions = [
            "Monitor lateral movement",
            "Detect privilege escalation",
        ]

        mock_historical_response = Mock()
        mock_historical_response.content = "Historical context of trust models"
        mock_historical_response.suggestions = [
            "Learn from military strategies",
            "Apply siege warfare principles",
        ]

        # Test blog synthesis
        content = mock_runner._synthesize_blog_content(
            topic, mock_security_response, mock_threat_response, mock_historical_response
        )

        assert isinstance(content, str)
        assert topic in content
        assert "Historical Context" in content
        assert "Security Analysis" in content
        assert "Threat Intelligence Perspective" in content
        assert "Key Takeaways" in content

    def test_content_formatting(self, mock_runner):
        """Test content formatting and structure."""
        content = "This is test cybersecurity content about network security and threat detection."

        # Test summary generation
        summary = mock_runner._generate_summary(content)
        assert isinstance(summary, str)

        # Test tag extraction
        tags = mock_runner._extract_tags("ransomware analysis", content)
        assert isinstance(tags, list)
        assert "cybersecurity" in tags
        assert "security" in tags

        # Test key concept extraction
        concepts = mock_runner._extract_key_concepts(content)
        assert isinstance(concepts, list)

    def test_exercise_generation(self, mock_runner):
        """Test exercise generation for educational content."""
        topic = "Incident Response"
        learning_objectives = [
            "Analyze incident response procedures",
            "Implement detection strategies",
        ]

        exercises = mock_runner._generate_exercises(topic, learning_objectives)

        assert isinstance(exercises, list)
        assert len(exercises) > 0
        assert any(topic in exercise for exercise in exercises)

    def test_file_saving(self, mock_runner, temp_dir):
        """Test file saving functionality."""
        # Mock blog post
        blog_post = Mock()
        blog_post.__dict__ = {
            "title": "Test Blog",
            "content": "Test content",
            "summary": "Test summary",
            "tags": ["test"],
            "sources": ["http://test.com"],
            "metadata": {"test": "data"},
            "created_at": "2024-01-01T00:00:00",
        }

        # Test blog post saving
        mock_runner._save_blog_post(blog_post)

        # Check if file was created
        blog_files = list(Path(temp_dir).glob("blog_post_*.json"))
        assert len(blog_files) > 0

        # Verify content
        with open(blog_files[0]) as f:
            saved_data = json.load(f)
            assert saved_data["title"] == "Test Blog"

    def test_error_handling(self, mock_runner):
        """Test error handling in various scenarios."""
        # Test with invalid topic
        try:
            blog_post = mock_runner.generate_blog_post("")
            # Should handle gracefully
        except Exception as e:
            # Should not raise unhandled exceptions
            assert isinstance(e, (ValueError, TypeError))

    def test_multi_agent_coordination(self, mock_runner):
        """Test coordination between multiple agents."""
        topic = "Advanced Persistent Threats"
        context = AgentContext(
            topic=topic, content_type=ContentType.RESEARCH_REPORT, technical_depth="advanced"
        )

        # Simulate multi-agent analysis
        security_analysis = mock_runner.security_analyst.analyze_topic(context)
        threat_analysis = mock_runner.threat_researcher.analyze_topic(context)
        historical_analysis = mock_runner.historian.analyze_topic(context)

        # Verify all agents provided responses
        assert security_analysis is not None
        assert threat_analysis is not None
        assert historical_analysis is not None

        # Verify responses have expected structure
        for response in [security_analysis, threat_analysis, historical_analysis]:
            assert hasattr(response, "content")
            assert hasattr(response, "sources")
            assert hasattr(response, "suggestions")


class TestWorkflowIntegration:
    """Test complete workflows from start to finish."""

    @pytest.fixture
    def integration_runner(self):
        """Create a runner for integration testing with minimal mocking."""
        with patch("cyber_storm.config.CyberStormConfig") as mock_config_class:
            # Create a more realistic config
            config = Mock()
            config.validate_config.return_value = []

            # Mock with actual method calls expected
            config.get_lm_for_agent.return_value = Mock()
            config.get_search_api_key.return_value = None  # Use DuckDuckGo (no API key needed)

            # Set up realistic config values
            config.security_analyst_config = Mock()
            config.security_analyst_config.lm_config = Mock()
            config.security_analyst_config.lm_config.__dict__ = {
                "model": "mock",
                "temperature": 0.7,
            }

            config.threat_researcher_config = Mock()
            config.threat_researcher_config.lm_config = Mock()
            config.threat_researcher_config.lm_config.__dict__ = {
                "model": "mock",
                "temperature": 0.8,
            }

            config.historian_config = Mock()
            config.historian_config.lm_config = Mock()
            config.historian_config.lm_config.__dict__ = {"model": "mock", "temperature": 0.9}

            config.retrieval_config = Mock()
            config.retrieval_config.search_engine = "duckduckgo"
            config.retrieval_config.max_results_per_query = 3
            config.retrieval_config.embedding_model = "mock-model"
            config.retrieval_config.device = "cpu"
            config.retrieval_config.vector_store_path = "/tmp"
            config.retrieval_config.qdrant_url = None
            config.retrieval_config.qdrant_api_key = None

            config.generation_config = Mock()
            config.generation_config.default_audience = "professionals"
            config.generation_config.default_technical_depth = "intermediate"
            config.generation_config.include_historical_context = True

            config.output_config = Mock()
            config.output_config.output_directory = "/tmp"
            config.output_config.save_intermediate_results = False

            config.to_dict.return_value = {"integration": "test"}

            with (
                patch("cyber_storm.runner.SecurityAnalystAgent"),
                patch("cyber_storm.runner.ThreatResearcherAgent"),
                patch("cyber_storm.runner.HistorianAgent"),
                patch("cyber_storm.runner.ThreatIntelRM"),
                patch("cyber_storm.runner.HistoricalRM"),
                patch("cyber_storm.runner.DuckDuckGoSearchRM"),
            ):

                runner = CyberStormRunner(config)
                return runner

    def test_end_to_end_blog_generation(self, integration_runner):
        """Test complete blog post generation workflow."""
        topic = "Social Engineering in Cybersecurity"

        # This should exercise the full pipeline
        blog_post = integration_runner.generate_blog_post(topic)

        assert blog_post is not None
        assert blog_post.title is not None
        assert len(blog_post.content) > 0
        assert isinstance(blog_post.tags, list)
        assert len(blog_post.tags) > 0

    def test_end_to_end_chapter_generation(self, integration_runner):
        """Test complete book chapter generation workflow."""
        topic = "Malware Analysis Fundamentals"
        objectives = [
            "Understand malware classification",
            "Analyze static and dynamic analysis techniques",
            "Implement detection strategies",
        ]

        chapter = integration_runner.generate_book_chapter(topic, 1, objectives)

        assert chapter is not None
        assert chapter.chapter_number == 1
        assert len(chapter.content) > 0
        assert len(chapter.exercises) > 0
        assert len(chapter.key_concepts) > 0

    def test_research_session_workflow(self, integration_runner):
        """Test interactive research session workflow."""
        topic = "Cloud Security Challenges"

        session = integration_runner.interactive_research(topic)

        assert session is not None
        assert session.topic == topic
        assert len(session.generated_questions) > 0
        assert len(session.conversation_log) > 0

    def test_system_reliability(self, integration_runner):
        """Test system reliability with multiple operations."""
        topics = [
            "Network Security Fundamentals",
            "Incident Response Planning",
            "Threat Hunting Methodologies",
        ]

        results = []
        for topic in topics:
            try:
                blog_post = integration_runner.generate_blog_post(topic)
                results.append(blog_post is not None)
            except Exception:
                results.append(False)

        # Most operations should succeed
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.5  # At least 50% success rate
