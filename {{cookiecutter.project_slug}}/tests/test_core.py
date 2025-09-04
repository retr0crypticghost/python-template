"""
Tests for the core module.
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from {{ cookiecutter.package_name }}.core import App


class TestApp:
    """Test cases for the App class."""

    def test_app_initialization(self):
        """Test that the App initializes correctly."""
        app = App()
        assert app is not None
        assert hasattr(app, 'config')
        assert hasattr(app, 'logger')

    @patch('{{ cookiecutter.package_name }}.core.load_dotenv')
    def test_app_loads_dotenv(self, mock_load_dotenv):
        """Test that the App loads environment variables."""
        App()
        mock_load_dotenv.assert_called_once()

    def test_process_data(self):
        """Test the _process_data method."""
        app = App()
        result = app._process_data()
        assert isinstance(result, int)
        assert result > 0

    @patch('{{ cookiecutter.package_name }}.core.App._process_data')
    def test_run_success(self, mock_process_data):
        """Test successful run of the application."""
        mock_process_data.return_value = 42

        app = App()
        app.run()  # Should not raise any exceptions
        mock_process_data.assert_called_once()

    @patch('{{ cookiecutter.package_name }}.core.App._process_data')
    def test_run_failure(self, mock_process_data):
        """Test that run properly handles exceptions."""
        mock_process_data.side_effect = RuntimeError("Test error")

        app = App()
        with pytest.raises(RuntimeError, match="Test error"):
            app.run()

    def test_parse_env_example_missing_file(self, temp_dir):
        """Test parsing when .env.example file doesn't exist."""
        app = App()

        # Point to a non-existent file
        non_existent_path = temp_dir / "non_existent.env"
        result = app._parse_env_example(non_existent_path)

        assert result == {}

    def test_parse_env_example_valid_file(self, temp_dir):
        """Test parsing a valid .env.example file."""
        # Create a sample .env.example file
        env_example_content = """# Database configuration
DATABASE_URL=postgresql://localhost/mydb

# API Configuration
API_KEY=your_api_key_here

# OPTIONAL
# Optional feature flag
FEATURE_ENABLED=false

# Another required variable
MAX_CONNECTIONS=10
"""
        env_example_path = temp_dir / ".env.example"
        env_example_path.write_text(env_example_content)

        app = App()
        result = app._parse_env_example(env_example_path)

        # Check that variables were parsed correctly
        assert "DATABASE_URL" in result
        assert "API_KEY" in result
        assert "FEATURE_ENABLED" in result
        assert "MAX_CONNECTIONS" in result

        # Check descriptions
        assert result["DATABASE_URL"]["description"] == "Database configuration"
        assert result["API_KEY"]["description"] == "API Configuration"

        # Check optional flag
        assert result["FEATURE_ENABLED"]["optional"] is True
        assert result["DATABASE_URL"]["optional"] is False

    @patch('{{ cookiecutter.package_name }}.core.os.getenv')
    def test_check_environment_with_vars(self, mock_getenv, temp_dir):
        """Test environment checking with some variables present."""
        # Create a simple .env.example
        env_example_content = """# Required variable
REQUIRED_VAR=value

# OPTIONAL
# Optional variable
OPTIONAL_VAR=value
"""
        env_example_path = temp_dir / ".env.example"
        env_example_path.write_text(env_example_content)

        # Mock environment variables
        def mock_getenv_side_effect(var_name, default=None):
            env_vars = {
                "REQUIRED_VAR": "present_value"
                # OPTIONAL_VAR is missing
            }
            return env_vars.get(var_name, default)

        mock_getenv.side_effect = mock_getenv_side_effect

        # Mock the path resolution to point to our temp file
        with patch.object(Path, 'parent', new_callable=lambda: temp_dir):
            App()  # Test that app initializes without errors
            # This should run without errors and log appropriately
            # The actual logging assertions would require capturing log output
