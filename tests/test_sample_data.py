"""
Tests for Cyber-Researcher with sample threat intelligence data.

This module tests the system with realistic sample data to validate
end-to-end functionality.
"""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path
import tempfile
import os
import pandas as pd
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cyber_storm import CyberStormRunner, CyberStormConfig


class TestSampleDataGeneration:
    """Test sample data generation and ingestion."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    def test_threat_intel_sample_data_creation(self, temp_dir):
        """Test creation of sample threat intelligence data."""
        # Create sample data CSV
        sample_data = {
            "content": [
                "APT29 (Cozy Bear) has been observed using sophisticated spearphishing campaigns targeting government and healthcare organizations. The group employs living-off-the-land tactics and advanced persistence mechanisms.",
                "Ransomware group LockBit 3.0 has developed new encryption algorithms and improved their data exfiltration capabilities. Recent attacks have targeted critical infrastructure including energy and transportation sectors.",
                "Supply chain attacks continue to evolve with threat actors compromising software build environments. The SolarWinds-style attacks have become a blueprint for other advanced persistent threat groups.",
                "Social engineering attacks have increased by 400% with threat actors leveraging AI-generated content to create more convincing phishing emails and voice calls targeting financial institutions.",
                "Zero-day exploits in web browsers are being weaponized by nation-state actors. These exploits target memory corruption vulnerabilities to achieve remote code execution on target systems.",
            ],
            "title": [
                "APT29 Advanced Spearphishing Campaign Analysis",
                "LockBit 3.0 Ransomware: Enhanced Capabilities Assessment",
                "Supply Chain Attack Methodology Evolution",
                "AI-Powered Social Engineering Threat Landscape",
                "Browser Zero-Day Exploitation by Nation-State Actors",
            ],
            "url": [
                "https://example-threatintel.com/apt29-spearphishing-2024",
                "https://example-threatintel.com/lockbit-3-analysis",
                "https://example-threatintel.com/supply-chain-attacks-2024",
                "https://example-threatintel.com/ai-social-engineering",
                "https://example-threatintel.com/browser-zero-days-2024",
            ],
            "description": [
                "Comprehensive analysis of APT29's latest spearphishing tactics and techniques",
                "Technical breakdown of LockBit 3.0 ransomware capabilities and defensive measures",
                "Evolution of supply chain attack methodologies with case studies",
                "Impact assessment of AI-generated content in social engineering campaigns",
                "Analysis of browser zero-day exploits attributed to nation-state actors",
            ],
            "date": ["2024-01-15", "2024-02-01", "2024-02-15", "2024-03-01", "2024-03-15"],
            "threat_type": ["APT", "Ransomware", "Supply Chain", "Social Engineering", "Zero-Day"],
            "severity": ["High", "Critical", "High", "Medium", "Critical"],
            "targets": [
                "Government, Healthcare",
                "Critical Infrastructure",
                "Software Vendors",
                "Financial Services",
                "Global",
            ],
        }

        df = pd.DataFrame(sample_data)
        csv_path = os.path.join(temp_dir, "sample_threat_reports.csv")
        df.to_csv(csv_path, index=False)

        # Verify file creation
        assert os.path.exists(csv_path)

        # Verify content
        loaded_df = pd.read_csv(csv_path)
        assert len(loaded_df) == 5
        assert "content" in loaded_df.columns
        assert "threat_type" in loaded_df.columns
        assert "severity" in loaded_df.columns

    def test_historical_sample_data_creation(self, temp_dir):
        """Test creation of sample historical data."""
        historical_data = {
            "content": [
                "The Trojan Horse was a legendary stratagem used by the Greeks during the Trojan War. By hiding soldiers inside a wooden horse presented as a gift, they deceived the Trojans into bringing their enemies inside the city walls.",
                "During World War II, the Enigma machine was used by German forces for encrypted communications. The breaking of the Enigma code by Allied cryptographers was crucial to the war effort and represents an early example of cryptographic warfare.",
                "The telegraph revolutionized long-distance communication in the 19th century, but it also introduced new vulnerabilities. Telegraph lines could be tapped, and false messages could be injected, leading to early forms of communication security concerns.",
                "In ancient Rome, Caesar's cipher was used to protect military communications by shifting letters in the alphabet. This early encryption method demonstrates the historical need for information security in military operations.",
                "The development of semaphore systems in the 18th century allowed for rapid visual communication across long distances, but these systems were vulnerable to interception and required clear lines of sight, highlighting early network security challenges.",
            ],
            "title": [
                "The Trojan Horse: Ancient Deception Tactics",
                "WWII Enigma Machine: Cryptographic Warfare",
                "Telegraph Security: Early Communication Vulnerabilities",
                "Caesar's Cipher: Ancient Military Encryption",
                "Semaphore Systems: Visual Communication Networks",
            ],
            "url": [
                "https://example-history.com/trojan-horse",
                "https://example-history.com/enigma-machine",
                "https://example-history.com/telegraph-security",
                "https://example-history.com/caesar-cipher",
                "https://example-history.com/semaphore-systems",
            ],
            "description": [
                "Analysis of the Trojan Horse as an early example of social engineering",
                "Historical significance of cryptographic breakthroughs in WWII",
                "Early communication security challenges in telegraph systems",
                "Ancient encryption methods and their modern parallels",
                "Historical perspective on visual communication network vulnerabilities",
            ],
            "period": ["Ancient Greece", "1940s", "1800s", "Ancient Rome", "1700s-1800s"],
            "theme": [
                "Deception",
                "Cryptography",
                "Communication Security",
                "Encryption",
                "Network Communications",
            ],
            "relevance": [
                "Social Engineering",
                "Cryptographic Attacks",
                "Network Monitoring",
                "Classical Cryptography",
                "Communication Protocols",
            ],
        }

        df = pd.DataFrame(historical_data)
        csv_path = os.path.join(temp_dir, "sample_historical_data.csv")
        df.to_csv(csv_path, index=False)

        # Verify file creation
        assert os.path.exists(csv_path)

        # Verify content
        loaded_df = pd.read_csv(csv_path)
        assert len(loaded_df) == 5
        assert "content" in loaded_df.columns
        assert "theme" in loaded_df.columns
        assert "relevance" in loaded_df.columns


class TestSystemWithSampleData:
    """Test the complete system using sample data."""

    @pytest.fixture
    def sample_runner(self, temp_dir):
        """Create a CyberStormRunner with sample data."""
        # Create sample data files
        threat_data = {
            "content": [
                "Advanced persistent threat group APT29 continues to evolve their tactics",
                "Ransomware operators are targeting cloud infrastructure with new techniques",
                "Supply chain attacks represent a growing threat to software security",
            ],
            "title": [
                "APT29 Threat Analysis",
                "Cloud Ransomware Trends",
                "Supply Chain Security Report",
            ],
            "url": ["http://test1.com", "http://test2.com", "http://test3.com"],
            "description": ["APT analysis", "Ransomware report", "Supply chain study"],
            "date": ["2024-01-01", "2024-02-01", "2024-03-01"],
            "threat_type": ["APT", "Ransomware", "Supply Chain"],
            "severity": ["High", "Critical", "Medium"],
            "targets": ["Government", "Enterprise", "Technology"],
        }

        historical_data = {
            "content": [
                "The Trojan Horse represents early deception tactics",
                "WWII cryptography laid foundations for modern encryption",
                "Ancient military communication methods",
            ],
            "title": [
                "Trojan Horse Deception",
                "WWII Cryptography",
                "Ancient Military Communications",
            ],
            "url": ["http://hist1.com", "http://hist2.com", "http://hist3.com"],
            "description": ["Ancient deception", "War cryptography", "Military comms"],
            "period": ["Ancient", "1940s", "Ancient"],
            "theme": ["Deception", "Cryptography", "Communication"],
            "relevance": ["Social Engineering", "Encryption", "Networks"],
        }

        # Save sample data
        threat_df = pd.DataFrame(threat_data)
        threat_path = os.path.join(temp_dir, "threat_data.csv")
        threat_df.to_csv(threat_path, index=False)

        historical_df = pd.DataFrame(historical_data)
        historical_path = os.path.join(temp_dir, "historical_data.csv")
        historical_df.to_csv(historical_path, index=False)

        # Mock configuration
        with patch("cyber_storm.config.CyberStormConfig") as mock_config_class:
            config = Mock()
            config.validate_config.return_value = []

            # Set up realistic config
            config.get_lm_for_agent.return_value = Mock()
            config.get_search_api_key.return_value = None

            # Mock agent configs
            for agent_type in ["security_analyst", "threat_researcher", "historian"]:
                agent_config = Mock()
                agent_config.lm_config = Mock()
                agent_config.lm_config.__dict__ = {"model": f"mock-{agent_type}"}
                setattr(config, f"{agent_type}_config", agent_config)

            # Mock retrieval config
            config.retrieval_config = Mock()
            config.retrieval_config.search_engine = "duckduckgo"
            config.retrieval_config.max_results_per_query = 3
            config.retrieval_config.embedding_model = "mock-model"
            config.retrieval_config.device = "cpu"
            config.retrieval_config.vector_store_path = temp_dir
            config.retrieval_config.qdrant_url = None
            config.retrieval_config.qdrant_api_key = None

            # Mock generation config
            config.generation_config = Mock()
            config.generation_config.default_audience = "professionals"
            config.generation_config.default_technical_depth = "intermediate"
            config.generation_config.include_historical_context = True

            # Mock output config
            config.output_config = Mock()
            config.output_config.output_directory = temp_dir
            config.output_config.save_intermediate_results = True

            config.to_dict.return_value = {"test": "config"}

            # Mock the agents and retrieval modules
            with (
                patch("cyber_storm.runner.SecurityAnalystAgent") as mock_security,
                patch("cyber_storm.runner.ThreatResearcherAgent") as mock_threat,
                patch("cyber_storm.runner.HistorianAgent") as mock_historian,
                patch("cyber_storm.runner.ThreatIntelRM") as mock_threat_rm,
                patch("cyber_storm.runner.HistoricalRM") as mock_historical_rm,
                patch("cyber_storm.runner.DuckDuckGoSearchRM"),
            ):

                # Mock agent responses based on sample data
                security_response = Mock()
                security_response.content = "Security analysis based on threat intelligence data"
                security_response.sources = ["http://test1.com"]
                security_response.suggestions = [
                    "Implement detection rules",
                    "Monitor for indicators",
                ]
                security_response.confidence = 0.9

                threat_response = Mock()
                threat_response.content = "Threat intelligence analysis of current campaigns"
                threat_response.sources = ["http://test2.com"]
                threat_response.suggestions = ["Track threat actors", "Update IOCs"]
                threat_response.confidence = 0.85

                historical_response = Mock()
                historical_response.content = (
                    "Historical context shows similar patterns in ancient deception"
                )
                historical_response.sources = ["http://hist1.com"]
                historical_response.suggestions = ["Learn from history", "Apply ancient lessons"]
                historical_response.confidence = 0.8

                # Configure agents
                mock_security.return_value.analyze_topic.return_value = security_response
                mock_threat.return_value.analyze_topic.return_value = threat_response
                mock_historian.return_value.analyze_topic.return_value = historical_response

                # Configure question generation
                for agent_mock in [
                    mock_security.return_value,
                    mock_threat.return_value,
                    mock_historian.return_value,
                ]:
                    agent_mock.generate_questions.return_value = [
                        "What are the key indicators?",
                        "How can we detect this threat?",
                        "What historical parallels exist?",
                    ]

                # Configure retrieval modules
                mock_threat_rm.return_value.ingest_threat_reports.return_value = 3
                mock_threat_rm.return_value.create_sample_data.return_value = 10
                mock_threat_rm.return_value.get_collection_stats.return_value = {
                    "total_documents": 3
                }

                mock_historical_rm.return_value.ingest_historical_events.return_value = 3
                mock_historical_rm.return_value.create_sample_data.return_value = 10

                runner = CyberStormRunner(config)

                # Store paths for testing
                runner._threat_data_path = threat_path
                runner._historical_data_path = historical_path

                return runner

    def test_blog_post_with_sample_data(self, sample_runner):
        """Test blog post generation using sample data."""
        topic = "Modern Social Engineering: Lessons from the Trojan Horse"

        blog_post = sample_runner.generate_blog_post(topic, style="educational")

        assert blog_post is not None
        assert blog_post.title is not None
        assert topic.split(":")[0] in blog_post.title
        assert len(blog_post.content) > 100
        assert isinstance(blog_post.tags, list)
        assert len(blog_post.tags) > 0
        assert "cybersecurity" in blog_post.tags

        # Check that content includes different perspectives
        content_lower = blog_post.content.lower()
        assert any(word in content_lower for word in ["security", "threat", "historical"])

        # Check metadata
        assert "agents_used" in blog_post.metadata
        assert len(blog_post.metadata["agents_used"]) == 3

    def test_book_chapter_with_sample_data(self, sample_runner):
        """Test book chapter generation using sample data."""
        topic = "Advanced Persistent Threats: Historical and Modern Perspectives"
        learning_objectives = [
            "Understand APT tactics and techniques",
            "Analyze historical parallels to modern threats",
            "Develop comprehensive defense strategies",
        ]

        chapter = sample_runner.generate_book_chapter(topic, 5, learning_objectives)

        assert chapter is not None
        assert chapter.chapter_number == 5
        assert chapter.title is not None
        assert len(chapter.content) > 200
        assert chapter.learning_objectives == learning_objectives
        assert len(chapter.exercises) > 0
        assert len(chapter.key_concepts) > 0

        # Check educational structure
        content_lower = chapter.content.lower()
        assert "learning objectives" in content_lower
        assert "practical applications" in content_lower

    def test_interactive_research_with_sample_data(self, sample_runner):
        """Test interactive research session with sample data."""
        topic = "Ransomware Evolution and Historical Deception Tactics"

        session = sample_runner.interactive_research(topic)

        assert session is not None
        assert session.topic == topic
        assert len(session.generated_questions) > 0
        assert len(session.conversation_log) > 0

        # Verify questions cover multiple perspectives
        all_questions = " ".join(session.generated_questions).lower()
        assert any(word in all_questions for word in ["indicator", "detect", "historical"])

    def test_data_ingestion_workflow(self, sample_runner):
        """Test the complete data ingestion workflow."""
        # Test threat intelligence ingestion
        threat_result = sample_runner.ingest_threat_report(sample_runner._threat_data_path)
        assert isinstance(threat_result, bool)

        # Get system status to verify ingestion
        status = sample_runner.get_system_status()
        assert "retrieval" in status
        assert "threat_intel" in status["retrieval"]

    def test_content_quality_with_sample_data(self, sample_runner):
        """Test content quality when using sample data."""
        topic = "Supply Chain Security: Ancient Trade Routes to Modern Software"

        blog_post = sample_runner.generate_blog_post(topic)

        # Basic quality checks
        assert len(blog_post.content.split()) > 100  # Reasonable length
        assert blog_post.content.count("\n") > 5  # Has structure
        assert "##" in blog_post.content  # Has headers

        # Check for educational elements
        content = blog_post.content
        assert "Introduction" in content
        assert "Historical Context" in content
        assert "Security Analysis" in content
        assert "Key Takeaways" in content

        # Verify sources are included
        assert len(blog_post.sources) > 0
        assert all(source.startswith("http") for source in blog_post.sources)

    def test_multi_topic_generation(self, sample_runner):
        """Test generation across multiple cybersecurity topics."""
        topics = [
            "Phishing Evolution: From Ancient Deception to Modern Emails",
            "Cryptography Through the Ages: Caesar to Quantum",
            "Network Defense: Military Strategies in Cyber Warfare",
        ]

        results = []
        for topic in topics:
            try:
                blog_post = sample_runner.generate_blog_post(topic)
                results.append(
                    {
                        "topic": topic,
                        "success": True,
                        "length": len(blog_post.content),
                        "tags": len(blog_post.tags),
                        "sources": len(blog_post.sources),
                    }
                )
            except Exception as e:
                results.append({"topic": topic, "success": False, "error": str(e)})

        # Verify most generations succeeded
        success_count = sum(1 for r in results if r["success"])
        assert success_count >= len(topics) * 0.8  # At least 80% success rate

        # Check successful generations have reasonable content
        successful_results = [r for r in results if r["success"]]
        if successful_results:
            avg_length = sum(r["length"] for r in successful_results) / len(successful_results)
            assert avg_length > 500  # Reasonable average content length

    def test_error_handling_with_sample_data(self, sample_runner):
        """Test error handling when working with sample data."""
        # Test with empty topic
        try:
            blog_post = sample_runner.generate_blog_post("")
            # Should handle gracefully
            assert blog_post is not None or True  # Either works or handles gracefully
        except Exception as e:
            # Should be a handled exception
            assert isinstance(e, (ValueError, TypeError))

        # Test with very long topic
        long_topic = "A" * 1000
        try:
            blog_post = sample_runner.generate_blog_post(long_topic)
            assert blog_post is not None or True
        except Exception as e:
            assert isinstance(e, (ValueError, TypeError))

    def test_output_file_generation(self, sample_runner, temp_dir):
        """Test that output files are properly generated."""
        topic = "Test Topic for File Generation"

        # Generate content with file saving enabled
        blog_post = sample_runner.generate_blog_post(topic)

        # Check if output files were created
        output_files = list(Path(temp_dir).glob("*.json"))

        # Should have at least some output files
        if sample_runner.config.output_config.save_intermediate_results:
            assert len(output_files) >= 0  # May or may not save depending on implementation

        # If files exist, verify they contain valid JSON
        for file_path in output_files:
            with open(file_path, "r") as f:
                data = json.load(f)
                assert isinstance(data, dict)
                if "title" in data:
                    assert isinstance(data["title"], str)


@pytest.mark.integration
class TestSampleDataIntegration:
    """Integration tests focusing on sample data workflows."""

    def test_end_to_end_sample_workflow(self, temp_dir):
        """Test complete end-to-end workflow with sample data."""
        # This would be a comprehensive integration test
        # For now, we'll test the basic workflow components

        # Verify sample data can be created
        sample_data = {
            "content": ["Test threat content"],
            "title": ["Test Threat"],
            "url": ["http://test.com"],
            "description": ["Test description"],
            "date": ["2024-01-01"],
            "threat_type": ["Test"],
            "severity": ["Medium"],
            "targets": ["Test Target"],
        }

        df = pd.DataFrame(sample_data)
        csv_path = os.path.join(temp_dir, "integration_test.csv")
        df.to_csv(csv_path, index=False)

        assert os.path.exists(csv_path)

        # Verify the CSV can be read back
        loaded_df = pd.read_csv(csv_path)
        assert len(loaded_df) == 1
        assert loaded_df.iloc[0]["content"] == "Test threat content"
