"""
Pytest configuration and shared fixtures for Cyber-Researcher tests.
"""

import pytest
import sys
from pathlib import Path
import tempfile
import os
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data that persists for the session."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_language_model():
    """Create a mock language model for testing."""
    mock_lm = Mock()
    mock_lm.generate.return_value = "Mock language model response for testing purposes."
    mock_lm.model_name = "mock-model"
    return mock_lm


@pytest.fixture
def mock_embedding_model():
    """Create a mock embedding model for testing."""
    with patch("sentence_transformers.SentenceTransformer") as mock_st:
        mock_model = Mock()
        mock_model.encode.return_value = [[0.1, 0.2, 0.3, 0.4, 0.5]]
        mock_st.return_value = mock_model
        yield mock_model


@pytest.fixture
def mock_vector_store():
    """Create a mock vector store for testing."""
    mock_store = Mock()
    mock_store.search.return_value = [
        {
            "id": "test_doc_1",
            "payload": {
                "content": "Test document content about cybersecurity",
                "title": "Test Security Document",
                "url": "https://example.com/test",
            },
            "score": 0.95,
        },
        {
            "id": "test_doc_2",
            "payload": {
                "content": "Another test document about threat intelligence",
                "title": "Threat Intel Report",
                "url": "https://example.com/threat",
            },
            "score": 0.87,
        },
    ]
    mock_store.add_documents.return_value = True
    mock_store.count.return_value = 100
    return mock_store


@pytest.fixture
def sample_agent_response():
    """Create a sample agent response for testing."""
    from cyber_storm.agents import AgentResponse

    return AgentResponse(
        content="This is a sample agent analysis of the cybersecurity topic.",
        sources=["https://example.com/source1", "https://example.com/source2"],
        confidence=0.85,
        suggestions=[
            "Implement multi-factor authentication",
            "Regular security awareness training",
            "Deploy endpoint detection and response",
        ],
        metadata={
            "agent_role": "test_agent",
            "analysis_type": "test_analysis",
            "processing_time": 1.23,
        },
    )


@pytest.fixture
def sample_agent_context():
    """Create a sample agent context for testing."""
    from cyber_storm.agents import AgentContext, ContentType

    return AgentContext(
        topic="Advanced Persistent Threats",
        content_type=ContentType.BLOG_POST,
        target_audience="security professionals",
        technical_depth="intermediate",
        narrative_style="educational",
        historical_focus=True,
        max_sources=5,
    )


@pytest.fixture
def sample_threat_data():
    """Create sample threat intelligence data for testing."""
    return [
        {
            "content": "APT29 has been observed using spearphishing emails with malicious attachments",
            "title": "APT29 Spearphishing Campaign Analysis",
            "url": "https://example.com/apt29-analysis",
            "description": "Detailed analysis of APT29 spearphishing tactics",
            "date": "2024-01-15",
            "threat_type": "APT",
            "severity": "High",
            "targets": "Government, Healthcare",
        },
        {
            "content": "Ransomware operators are increasingly targeting cloud infrastructure",
            "title": "Cloud-Focused Ransomware Trends",
            "url": "https://example.com/cloud-ransomware",
            "description": "Analysis of ransomware tactics against cloud services",
            "date": "2024-02-01",
            "threat_type": "Ransomware",
            "severity": "Critical",
            "targets": "Enterprise, Cloud Providers",
        },
        {
            "content": "Supply chain attacks continue to be a preferred method for advanced threat actors",
            "title": "Supply Chain Attack Methodology",
            "url": "https://example.com/supply-chain",
            "description": "Comprehensive analysis of supply chain attack vectors",
            "date": "2024-02-15",
            "threat_type": "Supply Chain",
            "severity": "High",
            "targets": "Software Vendors, Enterprise",
        },
    ]


@pytest.fixture
def sample_historical_data():
    """Create sample historical data for testing."""
    return [
        {
            "content": "The Trojan Horse was used to deceive enemies in ancient warfare by hiding soldiers inside a wooden horse",
            "title": "The Trojan Horse Deception",
            "url": "https://example.com/trojan-horse",
            "description": "Ancient deception tactics that parallel modern social engineering",
            "period": "Ancient Greece",
            "theme": "Deception",
            "relevance": "Social Engineering",
        },
        {
            "content": "During WWII, the Enigma machine was used for encrypted communications between German forces",
            "title": "WWII Enigma Cryptography",
            "url": "https://example.com/enigma",
            "description": "Historical cryptographic methods and their modern parallels",
            "period": "1940s",
            "theme": "Cryptography",
            "relevance": "Encryption",
        },
        {
            "content": "The telegraph revolutionized long-distance communication in the 19th century",
            "title": "Telegraph Communication Revolution",
            "url": "https://example.com/telegraph",
            "description": "Historical communication breakthrough with modern network parallels",
            "period": "1800s",
            "theme": "Communication",
            "relevance": "Network Communications",
        },
    ]


@pytest.fixture
def mock_cyber_storm_config():
    """Create a mock CyberStormConfig for testing."""
    config = Mock()

    # Mock validation
    config.validate_config.return_value = []

    # Mock agent configurations
    config.get_lm_for_agent.return_value = Mock()

    for agent_type in ["security_analyst", "threat_researcher", "historian"]:
        agent_config = Mock()
        agent_config.lm_config = Mock()
        agent_config.lm_config.__dict__ = {
            "model": f"mock-{agent_type}",
            "temperature": 0.7,
            "max_tokens": 1000,
        }
        setattr(config, f"{agent_type}_config", agent_config)

    # Mock retrieval configuration
    config.retrieval_config = Mock()
    config.retrieval_config.search_engine = "duckduckgo"
    config.retrieval_config.max_results_per_query = 5
    config.retrieval_config.embedding_model = "mock-embedding"
    config.retrieval_config.device = "cpu"
    config.retrieval_config.vector_store_path = "/tmp/test"
    config.retrieval_config.qdrant_url = None
    config.retrieval_config.qdrant_api_key = None

    # Mock generation configuration
    config.generation_config = Mock()
    config.generation_config.default_audience = "security professionals"
    config.generation_config.default_technical_depth = "intermediate"
    config.generation_config.include_historical_context = True

    # Mock output configuration
    config.output_config = Mock()
    config.output_config.output_directory = "/tmp/test_output"
    config.output_config.save_intermediate_results = False

    # Mock search API keys
    config.get_search_api_key.return_value = None

    config.to_dict.return_value = {"test": "configuration"}

    return config


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "unit: mark test as unit test")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add markers based on test file or test name
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)

        if "test_end_to_end" in item.name or "test_workflow" in item.name:
            item.add_marker(pytest.mark.slow)
            item.add_marker(pytest.mark.integration)

        if "test_" in item.name and "integration" not in item.nodeid:
            item.add_marker(pytest.mark.unit)


# Skip tests if required dependencies are not available
def pytest_runtest_setup(item):
    """Setup for individual test runs."""
    # Skip certain tests if optional dependencies are missing
    if "requires_internet" in item.keywords:
        pytest.importorskip("requests")

    if "requires_ml" in item.keywords:
        pytest.importorskip("sentence_transformers")
        pytest.importorskip("qdrant_client")
