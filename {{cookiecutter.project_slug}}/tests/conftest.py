"""
Test configuration for {{ cookiecutter.package_name }}.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add src directory to Python path for tests
src_dir = Path(__file__).parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    test_vars = {
        'TEST_VAR': 'test_value',
        'API_KEY': 'mock_api_key',
        'DEBUG': 'true'
    }

    # Store original values
    original_values = {}
    for key in test_vars:
        original_values[key] = os.getenv(key)

    # Set test values
    for key, value in test_vars.items():
        os.environ[key] = value

    yield test_vars

    # Restore original values
    for key, original_value in original_values.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value


@pytest.fixture
def sample_config_file(temp_dir):
    """Create a sample configuration file for testing."""
    config_content = """
{
    "api": {
        "timeout": 30,
        "max_retries": 3,
        "base_url": "https://api.example.com"
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
}
"""
    config_file = temp_dir / "config.json"
    config_file.write_text(config_content.strip())
    return config_file
