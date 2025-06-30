"""
Unit tests for Cyber-Researcher retrieval modules.

Tests the functionality of ThreatIntelRM and HistoricalRM classes.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import tempfile
import os
import pandas as pd

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cyber_storm.rm import ThreatIntelRM, HistoricalRM


class TestThreatIntelRM:
    """Test cases for ThreatIntelRM."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def sample_threat_data(self, temp_dir):
        """Create sample threat intelligence data."""
        data = {
            "content": [
                "This is a threat report about APT29 using spearphishing",
                "Ransomware campaign targeting healthcare sector",
                "Supply chain attack compromising software vendors",
            ],
            "title": [
                "APT29 Spearphishing Campaign",
                "Healthcare Ransomware Alert",
                "Supply Chain Compromise Analysis",
            ],
            "url": [
                "https://example.com/apt29",
                "https://example.com/ransomware",
                "https://example.com/supply-chain",
            ],
            "description": [
                "Analysis of APT29 tactics",
                "Recent ransomware targeting healthcare",
                "Supply chain attack methodology",
            ],
            "date": ["2024-01-01", "2024-01-15", "2024-02-01"],
            "threat_type": ["APT", "Ransomware", "Supply Chain"],
            "severity": ["High", "Critical", "Medium"],
            "targets": ["Government", "Healthcare", "Technology"],
        }

        df = pd.DataFrame(data)
        csv_path = os.path.join(temp_dir, "threat_reports.csv")
        df.to_csv(csv_path, index=False)
        return csv_path

    @pytest.fixture
    def threat_rm(self, temp_dir):
        """Create ThreatIntelRM instance for testing."""
        # Mock the embedding model to avoid actual model loading
        with patch("cyber_storm.rm.threat_intel_rm.SentenceTransformer") as mock_model:
            mock_model.return_value.encode.return_value = [[0.1, 0.2, 0.3]]

            rm = ThreatIntelRM(
                collection_name="test_threat_intel",
                embedding_model="mock-model",
                k=3,
                vector_store_path=temp_dir,
            )

            # Mock the vector store
            rm.vector_store = Mock()
            rm.vector_store.search.return_value = [
                {"id": "1", "payload": {"content": "test content", "title": "test"}, "score": 0.9}
            ]

            return rm

    def test_initialization(self, threat_rm):
        """Test ThreatIntelRM initialization."""
        assert threat_rm.collection_name == "test_threat_intel"
        assert threat_rm.k == 3
        assert threat_rm.embedding_model is not None

    def test_retrieve_basic(self, threat_rm):
        """Test basic retrieval functionality."""
        query = "APT29 spearphishing attack"
        results = threat_rm.retrieve(query)

        assert isinstance(results, list)
        assert len(results) <= threat_rm.k

        # Mock should return our test data
        if results:
            result = results[0]
            assert "content" in result
            assert "title" in result

    def test_retrieve_with_filters(self, threat_rm):
        """Test retrieval with threat type filters."""
        query = "ransomware"
        results = threat_rm.retrieve(query, threat_type="Ransomware")

        assert isinstance(results, list)
        # Results should be filtered by threat type

    def test_retrieve_by_severity(self, threat_rm):
        """Test retrieval filtered by severity."""
        query = "critical threats"
        results = threat_rm.retrieve(query, min_severity="high")

        assert isinstance(results, list)

    def test_ingest_threat_reports(self, threat_rm, sample_threat_data):
        """Test ingesting threat reports from CSV."""
        # Mock the ingestion process
        threat_rm.vector_store.add_documents = Mock(return_value=True)

        num_ingested = threat_rm.ingest_threat_reports(sample_threat_data)

        assert num_ingested >= 0
        threat_rm.vector_store.add_documents.assert_called_once()

    def test_create_sample_data(self, threat_rm, temp_dir):
        """Test sample data creation."""
        output_path = os.path.join(temp_dir, "sample_data.csv")

        num_samples = threat_rm.create_sample_data(output_path)

        assert num_samples > 0
        assert os.path.exists(output_path)

        # Verify the CSV has correct structure
        df = pd.read_csv(output_path)
        expected_columns = [
            "content",
            "title",
            "url",
            "description",
            "date",
            "threat_type",
            "severity",
            "targets",
        ]
        assert all(col in df.columns for col in expected_columns)

    def test_get_collection_stats(self, threat_rm):
        """Test collection statistics retrieval."""
        # Mock stats
        threat_rm.vector_store.count = Mock(return_value=100)

        stats = threat_rm.get_collection_stats()

        assert isinstance(stats, dict)
        assert "total_documents" in stats

    def test_search_by_threat_type(self, threat_rm):
        """Test searching by specific threat types."""
        results = threat_rm.search_by_threat_type("APT")

        assert isinstance(results, list)

    def test_search_by_target_sector(self, threat_rm):
        """Test searching by target sector."""
        results = threat_rm.search_by_target_sector("Healthcare")

        assert isinstance(results, list)

    def test_get_threat_timeline(self, threat_rm):
        """Test threat timeline retrieval."""
        timeline = threat_rm.get_threat_timeline("2024-01-01", "2024-12-31")

        assert isinstance(timeline, list)

    def test_error_handling(self, threat_rm):
        """Test error handling for invalid inputs."""
        # Test with empty query
        results = threat_rm.retrieve("")
        assert results == []

        # Test with invalid file path
        result = threat_rm.ingest_threat_reports("/nonexistent/path.csv")
        assert result == 0


class TestHistoricalRM:
    """Test cases for HistoricalRM."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def sample_historical_data(self, temp_dir):
        """Create sample historical data."""
        data = {
            "content": [
                "The Trojan Horse was used to deceive enemies in ancient warfare",
                "During WWII, cryptography was crucial for secure communications",
                "The telegraph revolutionized long-distance communication",
            ],
            "title": ["Trojan Horse Deception", "WWII Cryptography", "Telegraph Innovation"],
            "url": [
                "https://history.com/trojan",
                "https://history.com/crypto",
                "https://history.com/telegraph",
            ],
            "description": [
                "Ancient deception tactics",
                "Wartime cryptographic methods",
                "Communication revolution",
            ],
            "period": ["Ancient", "1940s", "1800s"],
            "theme": ["Deception", "Cryptography", "Communication"],
            "relevance": ["Social Engineering", "Encryption", "Networks"],
        }

        df = pd.DataFrame(data)
        csv_path = os.path.join(temp_dir, "historical_events.csv")
        df.to_csv(csv_path, index=False)
        return csv_path

    @pytest.fixture
    def historical_rm(self, temp_dir):
        """Create HistoricalRM instance for testing."""
        with patch("cyber_storm.rm.historical_rm.SentenceTransformer") as mock_model:
            mock_model.return_value.encode.return_value = [[0.1, 0.2, 0.3]]

            rm = HistoricalRM(
                collection_name="test_historical",
                embedding_model="mock-model",
                k=3,
                vector_store_path=temp_dir,
            )

            # Mock the vector store
            rm.vector_store = Mock()
            rm.vector_store.search.return_value = [
                {
                    "id": "1",
                    "payload": {"content": "historical content", "title": "test"},
                    "score": 0.9,
                }
            ]

            return rm

    def test_initialization(self, historical_rm):
        """Test HistoricalRM initialization."""
        assert historical_rm.collection_name == "test_historical"
        assert historical_rm.k == 3

    def test_retrieve_basic(self, historical_rm):
        """Test basic historical retrieval."""
        query = "ancient deception tactics"
        results = historical_rm.retrieve(query)

        assert isinstance(results, list)
        assert len(results) <= historical_rm.k

    def test_find_parallels(self, historical_rm):
        """Test finding historical parallels."""
        cyber_concept = "social engineering"
        parallels = historical_rm.find_parallels(cyber_concept)

        assert isinstance(parallels, list)

    def test_retrieve_by_period(self, historical_rm):
        """Test retrieval filtered by historical period."""
        results = historical_rm.retrieve_by_period("Ancient")

        assert isinstance(results, list)

    def test_retrieve_by_theme(self, historical_rm):
        """Test retrieval filtered by theme."""
        results = historical_rm.retrieve_by_theme("Cryptography")

        assert isinstance(results, list)

    def test_ingest_historical_events(self, historical_rm, sample_historical_data):
        """Test ingesting historical events."""
        historical_rm.vector_store.add_documents = Mock(return_value=True)

        num_ingested = historical_rm.ingest_historical_events(sample_historical_data)

        assert num_ingested >= 0

    def test_create_sample_data(self, historical_rm, temp_dir):
        """Test sample historical data creation."""
        output_path = os.path.join(temp_dir, "sample_historical.csv")

        num_samples = historical_rm.create_sample_data(output_path)

        assert num_samples > 0
        assert os.path.exists(output_path)

        # Verify CSV structure
        df = pd.read_csv(output_path)
        expected_columns = [
            "content",
            "title",
            "url",
            "description",
            "period",
            "theme",
            "relevance",
        ]
        assert all(col in df.columns for col in expected_columns)

    def test_get_narrative_framework(self, historical_rm):
        """Test narrative framework generation."""
        framework = historical_rm.get_narrative_framework("encryption", "ancient codes")

        assert isinstance(framework, dict)
        assert "historical_context" in framework
        assert "modern_parallel" in framework

    def test_suggest_storytelling_elements(self, historical_rm):
        """Test storytelling element suggestions."""
        elements = historical_rm.suggest_storytelling_elements("cryptography")

        assert isinstance(elements, list)
        assert len(elements) > 0

    def test_get_timeline_context(self, historical_rm):
        """Test timeline context retrieval."""
        context = historical_rm.get_timeline_context("1940s")

        assert isinstance(context, dict)
        assert "events" in context
        assert "significance" in context


class TestRetrievalIntegration:
    """Integration tests for retrieval modules."""

    @pytest.fixture
    def mock_retrieval_modules(self):
        """Create mock retrieval modules for integration testing."""
        with (
            patch("cyber_storm.rm.threat_intel_rm.SentenceTransformer"),
            patch("cyber_storm.rm.historical_rm.SentenceTransformer"),
        ):

            threat_rm = ThreatIntelRM(collection_name="test_threat", embedding_model="mock", k=3)

            historical_rm = HistoricalRM(
                collection_name="test_historical", embedding_model="mock", k=3
            )

            # Mock vector stores
            for rm in [threat_rm, historical_rm]:
                rm.vector_store = Mock()
                rm.vector_store.search.return_value = [
                    {"id": "1", "payload": {"content": "test", "title": "test"}, "score": 0.9}
                ]

            return threat_rm, historical_rm

    def test_cross_retrieval_coordination(self, mock_retrieval_modules):
        """Test coordination between threat intel and historical retrieval."""
        threat_rm, historical_rm = mock_retrieval_modules

        query = "social engineering attacks"

        # Get results from both modules
        threat_results = threat_rm.retrieve(query)
        historical_results = historical_rm.retrieve(query)

        assert isinstance(threat_results, list)
        assert isinstance(historical_results, list)

    def test_complementary_perspectives(self, mock_retrieval_modules):
        """Test that modules provide complementary perspectives."""
        threat_rm, historical_rm = mock_retrieval_modules

        # Threat RM should focus on technical/current threats
        threat_query = "APT techniques and tactics"
        threat_results = threat_rm.retrieve(threat_query)

        # Historical RM should provide context and parallels
        historical_query = "deception in warfare"
        historical_results = historical_rm.retrieve(historical_query)

        assert isinstance(threat_results, list)
        assert isinstance(historical_results, list)

    def test_retrieval_performance(self, mock_retrieval_modules):
        """Test retrieval performance and response times."""
        threat_rm, historical_rm = mock_retrieval_modules

        import time

        # Test multiple queries to check consistency
        queries = ["malware", "encryption", "network security", "social engineering"]

        for query in queries:
            start_time = time.time()

            threat_results = threat_rm.retrieve(query)
            historical_results = historical_rm.retrieve(query)

            end_time = time.time()

            # Basic performance check (should be fast with mocks)
            assert (end_time - start_time) < 1.0
            assert isinstance(threat_results, list)
            assert isinstance(historical_results, list)
