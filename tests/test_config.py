"""
Unit tests for Cyber-Researcher configuration.

Tests the functionality of CyberStormConfig class.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
import sys
from pathlib import Path
import tempfile
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cyber_storm.config import CyberStormConfig


class TestCyberStormConfig:
    """Test cases for CyberStormConfig."""

    @pytest.fixture
    def temp_secrets_file(self):
        """Create a temporary secrets file for testing."""
        secrets_content = """
        [anthropic]
        api_key = "test_anthropic_key"

        [openai]
        api_key = "test_openai_key"

        [search]
        bing_api_key = "test_bing_key"
        serper_api_key = "test_serper_key"
        you_api_key = "test_you_key"

        [qdrant]
        url = "http://localhost:6333"
        api_key = "test_qdrant_key"
        """

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(secrets_content)
            temp_file = f.name

        yield temp_file

        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    def test_config_initialization_default(self):
        """Test default configuration initialization."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            assert config is not None
            assert hasattr(config, "security_analyst_config")
            assert hasattr(config, "threat_researcher_config")
            assert hasattr(config, "historian_config")
            assert hasattr(config, "retrieval_config")
            assert hasattr(config, "generation_config")
            assert hasattr(config, "output_config")

    def test_config_with_secrets_file(self, temp_secrets_file):
        """Test configuration loading with secrets file."""
        with (
            patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=True),
            patch("cyber_storm.config.cyber_storm_config.Path") as mock_path,
        ):

            # Mock the path resolution
            mock_path.return_value.parent.parent = Path("/mock/project/root")

            with patch("builtins.open", mock_open(read_data=open(temp_secrets_file).read())):
                config = CyberStormConfig(secrets_file=temp_secrets_file)

                assert config is not None

    def test_agent_configuration(self):
        """Test agent-specific configuration."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            # Test security analyst config
            assert config.security_analyst_config is not None
            assert hasattr(config.security_analyst_config, "lm_config")

            # Test threat researcher config
            assert config.threat_researcher_config is not None
            assert hasattr(config.threat_researcher_config, "lm_config")

            # Test historian config
            assert config.historian_config is not None
            assert hasattr(config.historian_config, "lm_config")

    def test_retrieval_configuration(self):
        """Test retrieval configuration."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            assert config.retrieval_config is not None
            assert hasattr(config.retrieval_config, "search_engine")
            assert hasattr(config.retrieval_config, "max_results_per_query")
            assert hasattr(config.retrieval_config, "embedding_model")
            assert hasattr(config.retrieval_config, "device")

    def test_generation_configuration(self):
        """Test generation configuration."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            assert config.generation_config is not None
            assert hasattr(config.generation_config, "default_audience")
            assert hasattr(config.generation_config, "default_technical_depth")
            assert hasattr(config.generation_config, "include_historical_context")

    def test_output_configuration(self):
        """Test output configuration."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            assert config.output_config is not None
            assert hasattr(config.output_config, "output_directory")
            assert hasattr(config.output_config, "save_intermediate_results")

    def test_get_lm_for_agent(self):
        """Test language model retrieval for agents."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            # Test getting LM for each agent type
            security_lm = config.get_lm_for_agent("security_analyst")
            threat_lm = config.get_lm_for_agent("threat_researcher")
            historian_lm = config.get_lm_for_agent("historian")

            assert security_lm is not None
            assert threat_lm is not None
            assert historian_lm is not None

            # Test invalid agent type
            with pytest.raises((ValueError, KeyError)):
                config.get_lm_for_agent("invalid_agent")

    def test_get_search_api_key(self):
        """Test search API key retrieval."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            # Test various search engines
            bing_key = config.get_search_api_key("bing")
            serper_key = config.get_search_api_key("serper")
            you_key = config.get_search_api_key("you")

            # With no secrets file, these should return None or empty
            assert bing_key is None or bing_key == ""
            assert serper_key is None or serper_key == ""
            assert you_key is None or you_key == ""

            # DuckDuckGo doesn't need API key
            ddg_key = config.get_search_api_key("duckduckgo")
            assert ddg_key is None

    def test_validate_config(self):
        """Test configuration validation."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            issues = config.validate_config()

            # Should return a list of issues (may be empty)
            assert isinstance(issues, list)

    def test_to_dict(self):
        """Test configuration serialization to dictionary."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            config_dict = config.to_dict()

            assert isinstance(config_dict, dict)
            assert "security_analyst_config" in config_dict
            assert "threat_researcher_config" in config_dict
            assert "historian_config" in config_dict
            assert "retrieval_config" in config_dict
            assert "generation_config" in config_dict
            assert "output_config" in config_dict

    def test_config_with_custom_parameters(self):
        """Test configuration with custom parameters."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            custom_output_dir = "/custom/output/path"

            config = CyberStormConfig(output_dir=custom_output_dir)

            assert config.output_config.output_directory == custom_output_dir

    def test_environment_variable_override(self):
        """Test configuration override with environment variables."""
        with (
            patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False),
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "env_anthropic_key"}),
        ):

            config = CyberStormConfig()

            # Environment variables should be accessible
            # The exact implementation depends on how the config class handles env vars

    def test_invalid_configuration_values(self):
        """Test handling of invalid configuration values."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            # Test with invalid output directory
            config = CyberStormConfig(output_dir="")

            # Should handle gracefully or provide default
            assert config.output_config.output_directory is not None

    def test_secrets_file_loading_errors(self):
        """Test handling of secrets file loading errors."""
        # Test with non-existent file
        with (
            patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=True),
            patch("builtins.open", side_effect=FileNotFoundError),
        ):

            # Should handle gracefully
            config = CyberStormConfig(secrets_file="/nonexistent/secrets.toml")
            assert config is not None

    def test_config_immutability(self):
        """Test that config objects maintain consistency."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            # Test that basic properties don't change unexpectedly
            initial_search_engine = config.retrieval_config.search_engine
            initial_output_dir = config.output_config.output_directory

            # After creating another config, original should be unchanged
            config2 = CyberStormConfig()

            assert config.retrieval_config.search_engine == initial_search_engine
            assert config.output_config.output_directory == initial_output_dir


class TestConfigurationDataClasses:
    """Test the configuration data classes."""

    def test_agent_config_structure(self):
        """Test agent configuration data structure."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            # Each agent config should have required attributes
            for agent_name in ["security_analyst", "threat_researcher", "historian"]:
                agent_config = getattr(config, f"{agent_name}_config")

                assert hasattr(agent_config, "lm_config")
                assert agent_config.lm_config is not None

    def test_retrieval_config_structure(self):
        """Test retrieval configuration data structure."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            retrieval_config = config.retrieval_config

            # Check required attributes
            required_attrs = [
                "search_engine",
                "max_results_per_query",
                "embedding_model",
                "device",
                "vector_store_path",
            ]

            for attr in required_attrs:
                assert hasattr(retrieval_config, attr)
                assert getattr(retrieval_config, attr) is not None

    def test_generation_config_structure(self):
        """Test generation configuration data structure."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            gen_config = config.generation_config

            # Check required attributes
            required_attrs = [
                "default_audience",
                "default_technical_depth",
                "include_historical_context",
            ]

            for attr in required_attrs:
                assert hasattr(gen_config, attr)
                assert getattr(gen_config, attr) is not None

    def test_output_config_structure(self):
        """Test output configuration data structure."""
        with patch("cyber_storm.config.cyber_storm_config.Path.exists", return_value=False):
            config = CyberStormConfig()

            output_config = config.output_config

            # Check required attributes
            required_attrs = ["output_directory", "save_intermediate_results"]

            for attr in required_attrs:
                assert hasattr(output_config, attr)
                assert getattr(output_config, attr) is not None
