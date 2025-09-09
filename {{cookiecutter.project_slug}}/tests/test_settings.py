"""
Tests for typed configuration (Pydantic settings) functionality.

These tests only run when typed_config is enabled in cookiecutter options.
"""

import os
import tempfile
from pathlib import Path

import pytest

{%- if cookiecutter.typed_config == 'y' %}

from {{ cookiecutter.package_name }}.settings import (
    ApiSettings,
    AppSettings,
    DatabaseSettings,
    FeatureSettings,
    LoggingSettings,
    SecuritySettings,
    Settings,
    get_settings,
)


class TestTypedSettings:
    """Test suite for typed Pydantic settings."""

    def test_default_settings(self):
        """Test that default settings load correctly."""
        settings = Settings()
        
        assert settings.app.name == "{{ cookiecutter.package_name }}"
        assert settings.app.version == "1.0.0"
        assert settings.app.debug is False
        
        assert settings.logging.level == "INFO"
        assert settings.logging.format == "json"
        
        assert settings.api.timeout == 30
        assert settings.api.max_retries == 3
        
        assert settings.features.caching is True
        assert settings.features.metrics is False

    def test_environment_variable_loading(self, monkeypatch):
        """Test that environment variables are loaded correctly."""
        # Set environment variables with the correct prefix
        monkeypatch.setenv("{{ cookiecutter.package_name|upper }}_APP__NAME", "test-app")
        monkeypatch.setenv("{{ cookiecutter.package_name|upper }}_APP__DEBUG", "true")
        monkeypatch.setenv("{{ cookiecutter.package_name|upper }}_LOGGING__LEVEL", "DEBUG")
        monkeypatch.setenv("{{ cookiecutter.package_name|upper }}_API__TIMEOUT", "60")
        monkeypatch.setenv("{{ cookiecutter.package_name|upper }}_FEATURES__CACHING", "false")
        
        settings = Settings()
        
        assert settings.app.name == "test-app"
        assert settings.app.debug is True
        assert settings.logging.level == "DEBUG"
        assert settings.api.timeout == 60
        assert settings.features.caching is False

    def test_dotenv_file_loading(self, tmp_path):
        """Test that .env file is loaded correctly."""
        env_file = tmp_path / ".env"
        env_file.write_text("""
{{ cookiecutter.package_name|upper }}_APP__NAME=env-test-app
{{ cookiecutter.package_name|upper }}_APP__DEBUG=true
{{ cookiecutter.package_name|upper }}_LOGGING__LEVEL=WARNING
{{ cookiecutter.package_name|upper }}_API__MAX_RETRIES=5
""")
        
        # Change to temp directory so .env is found
        original_cwd = Path.cwd()
        os.chdir(tmp_path)
        
        try:
            settings = Settings()
            assert settings.app.name == "env-test-app"
            assert settings.app.debug is True
            assert settings.logging.level == "WARNING"
            assert settings.api.max_retries == 5
        finally:
            os.chdir(original_cwd)

    def test_validation_errors(self):
        """Test that validation errors are raised for invalid values."""
        with pytest.raises(ValueError, match="Log level must be one of"):
            LoggingSettings(level="INVALID")
        
        with pytest.raises(ValueError, match="Log format must be"):
            LoggingSettings(format="invalid")
        
        with pytest.raises(ValueError, match="Security keys must be at least"):
            SecuritySettings(secret_key="short")

    def test_legacy_dict_compatibility(self):
        """Test that settings can be converted to legacy dict format."""
        settings = Settings()
        legacy_dict = settings.get_legacy_dict()
        
        assert isinstance(legacy_dict, dict)
        assert "app" in legacy_dict
        assert "logging" in legacy_dict
        assert "api" in legacy_dict
        assert "database" in legacy_dict
        assert "security" in legacy_dict
        assert "features" in legacy_dict
        
        # Check nested structure
        assert legacy_dict["app"]["name"] == "{{ cookiecutter.package_name }}"
        assert legacy_dict["logging"]["level"] == "INFO"
        assert legacy_dict["api"]["timeout"] == 30

    def test_get_settings_singleton(self):
        """Test that get_settings returns a singleton."""
        # Clear cache first
        get_settings.cache_clear()
        
        settings1 = get_settings()
        settings2 = get_settings()
        
        # Should be the same object due to caching
        assert settings1 is settings2

    def test_convenience_functions(self):
        """Test convenience functions for accessing settings sections."""
        from {{ cookiecutter.package_name }}.settings import (
            get_api_config,
            get_app_config,
            get_database_config,
            get_feature_config,
            get_logging_config,
            get_security_config,
        )
        
        app_config = get_app_config()
        assert isinstance(app_config, AppSettings)
        assert app_config.name == "{{ cookiecutter.package_name }}"
        
        logging_config = get_logging_config()
        assert isinstance(logging_config, LoggingSettings)
        assert logging_config.level == "INFO"
        
        api_config = get_api_config()
        assert isinstance(api_config, ApiSettings)
        assert api_config.timeout == 30
        
        db_config = get_database_config()
        assert isinstance(db_config, DatabaseSettings)
        assert db_config.pool_size == 5
        
        security_config = get_security_config()
        assert isinstance(security_config, SecuritySettings)
        
        feature_config = get_feature_config()
        assert isinstance(feature_config, FeatureSettings)
        assert feature_config.caching is True


{%- else %}

# Placeholder tests when typed_config is disabled
def test_typed_config_disabled():
    """Test that typed config is disabled."""
    # This is a placeholder test that always passes
    # when typed_config is disabled
    assert True

{%- endif %}