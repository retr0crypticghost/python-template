"""
Typed configuration settings for {{ cookiecutter.package_name }} using Pydantic.

This module provides type-safe configuration management with automatic validation,
environment variable loading, and IDE autocompletion support.
"""

from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import get_logger

logger = get_logger(__name__)


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    
    level: str = Field(default="INFO", description="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    format: str = Field(default="json", description="Log format (json or plain)")
    console_level: str = Field(default="INFO", description="Console log level")
    file_level: str = Field(default="DEBUG", description="File log level")
    file_path: str = Field(default="logs/{{ cookiecutter.package_name }}.log", description="Log file path")
    max_file_size: str = Field(default="10MB", description="Maximum log file size")
    backup_count: int = Field(default=5, description="Number of backup log files")
    
    @field_validator('level', 'console_level', 'file_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level values."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return v.upper()
    
    @field_validator('format')
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        """Validate log format values."""
        if v not in ["json", "plain"]:
            raise ValueError("Log format must be 'json' or 'plain'")
        return v


class ApiSettings(BaseSettings):
    """API configuration settings."""
    
    timeout: int = Field(default=30, description="API request timeout in seconds", ge=1)
    max_retries: int = Field(default=3, description="Maximum number of retries", ge=0)
    retry_delay: float = Field(default=1.0, description="Delay between retries in seconds", ge=0)
    base_url: str | None = Field(default=None, description="Base URL for API requests")


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    url: str | None = Field(default=None, description="Database connection URL")
    pool_size: int = Field(default=5, description="Connection pool size", ge=1)
    max_overflow: int = Field(default=10, description="Maximum pool overflow", ge=0)
    pool_timeout: int = Field(default=30, description="Pool timeout in seconds", ge=1)


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    secret_key: str | None = Field(default=None, description="Secret key for encryption")
    encryption_key: str | None = Field(default=None, description="Encryption key")
    
    @field_validator('secret_key', 'encryption_key')
    @classmethod
    def validate_key_length(cls, v: str | None) -> str | None:
        """Validate key lengths for security."""
        if v is not None and len(v) < 32:
            raise ValueError("Security keys must be at least 32 characters long")
        return v


class FeatureSettings(BaseSettings):
    """Feature flag settings."""
    
    caching: bool = Field(default=True, description="Enable caching")
    metrics: bool = Field(default=False, description="Enable metrics collection")


class AppSettings(BaseSettings):
    """Application settings."""
    
    name: str = Field(default="{{ cookiecutter.package_name }}", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")


class Settings(BaseSettings):
    """Main settings class combining all configuration sections."""
    
    model_config = SettingsConfigDict(
        # Load from environment variables with prefix
        env_prefix="{{ cookiecutter.package_name|upper }}_",
        env_nested_delimiter="__",  # Use double underscore for nested settings
        # Load from .env file
        env_file=".env",
        env_file_encoding="utf-8",
        # Case sensitivity
        case_sensitive=False,
        # Allow extra fields for extensibility
        extra="allow",
    )
    
    # Configuration sections
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    features: FeatureSettings = Field(default_factory=FeatureSettings)
    app: AppSettings = Field(default_factory=AppSettings)
    
    def __init__(self, **kwargs):
        """Initialize settings with config file loading."""
        super().__init__(**kwargs)
        logger.info("✅ Typed configuration loaded successfully")
    
    def get_legacy_dict(self) -> dict[str, Any]:
        """
        Convert to legacy dictionary format for compatibility.
        
        This method provides backward compatibility with the existing
        config.py module's dictionary-based access patterns.
        """
        return {
            "logging": self.logging.model_dump(),
            "api": self.api.model_dump(),
            "database": self.database.model_dump(),
            "security": self.security.model_dump(),
            "features": self.features.model_dump(),
            "app": self.app.model_dump(),
        }


@lru_cache()
def get_settings() -> Settings:
    """
    Get the global settings instance (cached singleton).
    
    Returns:
        Settings: The typed settings instance
    """
    return Settings()


# Convenience functions for common access patterns
def get_logging_config() -> LoggingSettings:
    """Get logging configuration."""
    return get_settings().logging


def get_api_config() -> ApiSettings:
    """Get API configuration."""
    return get_settings().api


def get_database_config() -> DatabaseSettings:
    """Get database configuration."""
    return get_settings().database


def get_security_config() -> SecuritySettings:
    """Get security configuration."""
    return get_settings().security


def get_feature_config() -> FeatureSettings:
    """Get feature flags."""
    return get_settings().features


def get_app_config() -> AppSettings:
    """Get application configuration."""
    return get_settings().app