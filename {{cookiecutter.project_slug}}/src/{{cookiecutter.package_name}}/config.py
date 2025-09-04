"""
Configuration management module for {{ cookiecutter.package_name }}.

This module handles hierarchical configuration loading:
DEFAULTS < CONFIG_FILE < Environment Variables

Environment variables take precedence over config file, which takes precedence over defaults.
"""

import os
from pathlib import Path
from typing import Any, ClassVar

import yaml

from .logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class Config:
    """Configuration manager with hierarchical loading and environment variable support."""

    # Default configuration values
    DEFAULT_CONFIG: ClassVar[dict[str, Any]] = {
        'logging': {
            'level': 'INFO',
            'format': 'json',
            'console_level': 'INFO',
            'file_level': 'DEBUG',
            'file_path': 'logs/{{ cookiecutter.package_name }}.log',
            'max_file_size': '10MB',
            'backup_count': 5
        },
        'api': {
            'timeout': 30,
            'max_retries': 3,
            'retry_delay': 1,
            'base_url': None
        },
        'database': {
            'url': None,
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 30
        },
        'security': {
            'secret_key': None,
            'encryption_key': None
        },
        'features': {
            'caching': True,
            'metrics': False
        },
        'app': {
            'name': '{{ cookiecutter.package_name }}',
            'version': '1.0.0',
            'debug': False
        }
    }

    def __init__(self, config_file: str | None = None, config_file_env_var: str = '{{ cookiecutter.package_name|upper }}_CONFIG_FILE'):
        """
        Initialize the configuration manager.

        Args:
            config_file: Direct path to config file (overrides environment variable)
            config_file_env_var: Environment variable name that contains the config file path
        """
        self.config_file = config_file
        self.config_file_env_var = config_file_env_var
        self.logger = get_logger(f"{__name__}.{self.__class__.__name__}")
        self._config: dict[str, Any] = {}
        self._load_configuration()

    def _load_configuration(self):
        """Load configuration from defaults, config file, and environment variables."""
        self.logger.info("Loading configuration hierarchy...")

        # Start with defaults
        self._config = self._deep_copy_dict(self.DEFAULT_CONFIG)
        self.logger.debug("✅ Loaded default configuration")

        # Load from config file if specified (direct file takes precedence over env var)
        config_file_path = self.config_file or os.getenv(self.config_file_env_var)
        if config_file_path:
            self._load_config_file(config_file_path)
        else:
            self.logger.debug(f"No config file specified in {self.config_file_env_var}")

        # Override with environment variables
        self._load_environment_overrides()

        self.logger.info("Configuration loading complete")

    def _load_config_file(self, config_file_path: str):
        """Load configuration from YAML or JSON file (auto-detected by extension)."""
        try:
            config_path = Path(config_file_path)

            if not config_path.exists():
                self.logger.warning(f"⚠️  Config file not found: {config_file_path}")
                return

            if not config_path.is_file():
                self.logger.warning(f"⚠️  Config path is not a file: {config_file_path}")
                return

            with open(config_path, encoding='utf-8') as f:
                # Auto-detect format by file extension
                file_extension = config_path.suffix.lower()
                if file_extension in ['.yaml', '.yml']:
                    file_config = yaml.safe_load(f)
                    format_name = "YAML"
                elif file_extension == '.json':
                    import json  # noqa: PLC0415
                    file_config = json.load(f)
                    format_name = "JSON"
                else:
                    # Default to YAML for unknown extensions
                    self.logger.debug(f"Unknown extension {file_extension}, attempting YAML parsing")
                    file_config = yaml.safe_load(f)
                    format_name = "YAML"

            if file_config is None:
                self.logger.warning(f"⚠️  Config file is empty: {config_file_path}")
                return

            if not isinstance(file_config, dict):
                self.logger.error(f"❌ Config file must contain a dictionary: {config_file_path}")
                return

            # Merge file config into current config
            self._deep_merge_dict(self._config, file_config)
            self.logger.info(f"✅ Loaded config file: {config_file_path} ({format_name} format)")

        except yaml.YAMLError as e:
            self.logger.error(f"❌ Error parsing YAML config file {config_file_path}: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Error parsing JSON config file {config_file_path}: {e}")
        except Exception as e:
            self.logger.error(f"❌ Error loading config file {config_file_path}: {e}")

    def _load_environment_overrides(self):
        """
        Load environment variable overrides using a mapping system.
        
        All environment variables follow the pattern: {{cookiecutter.package_name.upper()}}_VARIABLE_NAME
        This ensures consistent naming and avoids conflicts with system variables.
        """
        # Define environment variable mappings to config paths
        env_mappings = {
            # Logging configuration
            '{{ cookiecutter.package_name|upper }}_LOG_LEVEL': 'logging.level',
            '{{ cookiecutter.package_name|upper }}_LOG_FORMAT': 'logging.format',
            '{{ cookiecutter.package_name|upper }}_CONSOLE_LOG_LEVEL': 'logging.console_level',
            '{{ cookiecutter.package_name|upper }}_FILE_LOG_LEVEL': 'logging.file_level',
            '{{ cookiecutter.package_name|upper }}_LOG_FILE_PATH': 'logging.file_path',
            '{{ cookiecutter.package_name|upper }}_LOG_MAX_FILE_SIZE': 'logging.max_file_size',
            '{{ cookiecutter.package_name|upper }}_LOG_BACKUP_COUNT': 'logging.backup_count',

            # API configuration
            '{{ cookiecutter.package_name|upper }}_API_TIMEOUT': 'api.timeout',
            '{{ cookiecutter.package_name|upper }}_MAX_RETRIES': 'api.max_retries',
            '{{ cookiecutter.package_name|upper }}_RETRY_DELAY': 'api.retry_delay',
            '{{ cookiecutter.package_name|upper }}_API_BASE_URL': 'api.base_url',

            # Database configuration
            '{{ cookiecutter.package_name|upper }}_DATABASE_URL': 'database.url',
            '{{ cookiecutter.package_name|upper }}_DB_POOL_SIZE': 'database.pool_size',
            '{{ cookiecutter.package_name|upper }}_DB_MAX_OVERFLOW': 'database.max_overflow',
            '{{ cookiecutter.package_name|upper }}_DB_POOL_TIMEOUT': 'database.pool_timeout',

            # Security configuration
            '{{ cookiecutter.package_name|upper }}_SECRET_KEY': 'security.secret_key',
            '{{ cookiecutter.package_name|upper }}_ENCRYPTION_KEY': 'security.encryption_key',

            # Feature flags
            '{{ cookiecutter.package_name|upper }}_ENABLE_CACHING': 'features.caching',
            '{{ cookiecutter.package_name|upper }}_ENABLE_METRICS': 'features.metrics',

            # App configuration
            '{{ cookiecutter.package_name|upper }}_APP_NAME': 'app.name',
            '{{ cookiecutter.package_name|upper }}_APP_VERSION': 'app.version',
            '{{ cookiecutter.package_name|upper }}_DEBUG': 'app.debug'
        }

        override_count = 0
        for env_var, config_path in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # Convert string values to appropriate types
                converted_value = self._convert_env_value(env_value, config_path)
                self._set_nested_value(self._config, config_path, converted_value)
                self.logger.debug(f"✅ Environment override: {env_var} -> {config_path} = {converted_value}")
                override_count += 1

        if override_count > 0:
            self.logger.info(f"✅ Applied {override_count} environment variable override(s)")
        else:
            self.logger.debug("No environment variable overrides found")

    def _convert_env_value(self, value: str, config_path: str) -> Any:  # noqa: PLR0911
        """Convert environment variable string to appropriate type based on config path."""
        # Handle boolean values
        if config_path.endswith('.debug') or 'debug' in config_path.lower():
            return value.lower() in ('true', '1', 'yes', 'on')

        # Handle integer values
        if any(key in config_path for key in ['timeout', 'retries', 'pool_size', 'overflow', 'count']):
            try:
                return int(value)
            except ValueError:
                self.logger.warning(f"⚠️  Could not convert '{value}' to integer for {config_path}, using string")
                return value

        # Handle float values for file sizes
        if 'file_size' in config_path:
            try:
                # Handle sizes like "10MB", "1GB", etc.
                if value.upper().endswith('MB'):
                    return float(value[:-2]) * 1024 * 1024
                elif value.upper().endswith('GB'):
                    return float(value[:-2]) * 1024 * 1024 * 1024
                elif value.upper().endswith('KB'):
                    return float(value[:-2]) * 1024
                else:
                    return float(value)
            except ValueError:
                self.logger.warning(f"⚠️  Could not convert '{value}' to file size for {config_path}, using string")
                return value

        # Default to string
        return value

    def _set_nested_value(self, config_dict: dict, path: str, value: Any):
        """Set a nested dictionary value using dot notation path."""
        keys = path.split('.')
        current = config_dict

        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # Set the final value
        current[keys[-1]] = value

    def _deep_copy_dict(self, source: dict) -> dict[str, Any]:
        """Create a deep copy of a dictionary."""
        result: dict[str, Any] = {}
        for key, value in source.items():
            if isinstance(value, dict):
                result[key] = self._deep_copy_dict(value)
            else:
                result[key] = value
        return result

    def _deep_merge_dict(self, target: dict, source: dict):
        """Deep merge source dictionary into target dictionary."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge_dict(target[key], value)
            else:
                target[key] = value

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.

        Args:
            path: Dot-separated path to the config value (e.g., 'logging.level')
            default: Default value if path not found

        Returns:
            Configuration value or default
        """
        keys = path.split('.')
        current = self._config

        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default

    def get_section(self, section: str) -> dict[str, Any]:
        """
        Get an entire configuration section.

        Args:
            section: Section name (e.g., 'logging', 'api')

        Returns:
            Dictionary containing the section configuration
        """
        return self._config.get(section, {})

    def get_all(self) -> dict[str, Any]:
        """Get the entire configuration dictionary."""
        return self._deep_copy_dict(self._config)

    def reload(self):
        """Reload configuration from all sources."""
        self.logger.info("Reloading configuration...")
        self._load_configuration()

    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access to config sections."""
        return self._config[key]

    def __contains__(self, key: str) -> bool:
        """Check if a configuration section exists."""
        return key in self._config


# Global configuration instance
_config_instance: Config | None = None


def get_config() -> Config:
    """
    Get the global configuration instance (singleton pattern).

    Returns:
        Config: The global configuration instance
    """
    global _config_instance  # noqa: PLW0603
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def reload_config():
    """Force reload of the configuration (useful for testing or config changes)."""
    global _config_instance  # noqa: PLW0603
    _config_instance = Config()
