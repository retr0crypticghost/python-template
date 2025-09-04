"""
Tests for the configuration module.
"""

from unittest.mock import patch

from {{ cookiecutter.package_name }}.config import Config, get_config


class TestConfig:
    """Tests for the Config class."""

    def test_config_initialization(self):
        """Test that Config initializes with defaults."""
        config = Config()
        assert config is not None
        # Should have some default values
        assert config.get('logging.level') is not None

    def test_config_with_file(self, sample_config_file):
        """Test loading configuration from file."""
        config = Config(config_file=str(sample_config_file))

        # Check that values from file are loaded
        assert config.get('api.timeout') == 30
        assert config.get('api.max_retries') == 3
        assert config.get('api.base_url') == "https://api.example.com"

    def test_config_with_env_vars(self):
        """Test that environment variables override configuration."""
        with patch.dict('os.environ', {'{{cookiecutter.package_name|upper}}_API_TIMEOUT': '60'}):
            config = Config()
            # Environment variable should override default (converted to int)
            assert config.get('api.timeout') == 60

    def test_config_hierarchy(self, sample_config_file):
        """Test configuration hierarchy: env vars > config file > defaults."""

        with patch.dict('os.environ', {'{{cookiecutter.package_name|upper}}_API_TIMEOUT': '90'}):
            config = Config(config_file=str(sample_config_file))

            # Environment variable should win (converted to int)
            assert config.get('api.timeout') == 90

            # File value should be used when no env var
            assert config.get('api.max_retries') == 3

            # Default should be used when neither file nor env var
            assert config.get('logging.level') is not None

    def test_get_config_singleton(self):
        """Test that get_config returns a singleton."""

        config1 = get_config()
        config2 = get_config()

        assert config1 is config2

    def test_config_get_with_default(self):
        """Test getting configuration values with defaults."""

        config = Config()

        # Non-existent key should return default
        assert config.get('non.existent.key', 'default_value') == 'default_value'

        # Non-existent key without default should return None
        assert config.get('another.non.existent.key') is None

    def test_config_invalid_file(self, temp_dir):
        """Test handling of invalid configuration file."""

        # Create an invalid JSON file
        invalid_config = temp_dir / "invalid_config.json"
        invalid_config.write_text("{ invalid json content")

        # Should not raise exception, but log error and use defaults
        config = Config(config_file=str(invalid_config))
        assert config is not None
        # Should still have default values
        assert config.get('logging.level') is not None

    def test_config_missing_file(self):
        """Test handling when configuration file doesn't exist."""

        # Should not raise exception
        config = Config(config_file="non_existent_file.json")
        assert config is not None
        # Should still have default values
        assert config.get('logging.level') is not None

    def test_config_directory_instead_of_file(self, temp_dir):
        """Test handling when config path points to directory instead of file."""

        # Create a directory instead of a file
        config_dir = temp_dir / "config_dir"
        config_dir.mkdir()

        # Should not raise exception, but log warning and use defaults
        config = Config(config_file=str(config_dir))
        assert config is not None
        # Should still have default values
        assert config.get('logging.level') is not None

    def test_config_yaml_file_loading(self, temp_dir):
        """Test loading configuration from YAML file."""

        # Create a YAML config file
        yaml_config_content = """
api:
  timeout: 45
  max_retries: 5
  base_url: "https://yaml.example.com"
logging:
  level: "WARNING"
"""
        yaml_config_file = temp_dir / "config.yaml"
        yaml_config_file.write_text(yaml_config_content.strip())

        config = Config(config_file=str(yaml_config_file))

        # Check that YAML values are loaded
        assert config.get('api.timeout') == 45
        assert config.get('api.max_retries') == 5
        assert config.get('api.base_url') == "https://yaml.example.com"
        assert config.get('logging.level') == "WARNING"

    def test_config_unknown_extension_fallback_to_yaml(self, temp_dir):
        """Test that unknown file extensions fallback to YAML parsing."""

        # Create a file with unknown extension but YAML content
        unknown_config_content = """
api:
  timeout: 99
  unknown_format: true
"""
        unknown_config_file = temp_dir / "config.unknown"
        unknown_config_file.write_text(unknown_config_content.strip())

        config = Config(config_file=str(unknown_config_file))

        # Should parse as YAML and load values
        assert config.get('api.timeout') == 99
        assert config.get('api.unknown_format') is True

    def test_config_empty_file_handling(self, temp_dir):
        """Test handling of empty configuration files."""

        # Create an empty file
        empty_config_file = temp_dir / "empty.yaml"
        empty_config_file.write_text("")

        # Should not raise exception, use defaults
        config = Config(config_file=str(empty_config_file))
        assert config is not None
        # Should still have default values
        assert config.get('logging.level') is not None

    def test_config_non_dict_content(self, temp_dir):
        """Test handling when config file contains non-dictionary content."""

        # Create a file with non-dict content (a list)
        list_config_content = """
- item1
- item2
- item3
"""
        list_config_file = temp_dir / "list_config.yaml"
        list_config_file.write_text(list_config_content.strip())

        # Should not raise exception, use defaults
        config = Config(config_file=str(list_config_file))
        assert config is not None
        # Should still have default values
        assert config.get('logging.level') is not None

    def test_config_env_variable_type_conversion(self):
        """Test environment variable type conversion."""

        with patch.dict('os.environ', {
            '{{ cookiecutter.package_name|upper }}_API_TIMEOUT': '120',  # Should convert to int
            '{{ cookiecutter.package_name|upper }}_DEBUG': 'true',  # Should convert to bool
            '{{ cookiecutter.package_name|upper }}_LOG_MAX_FILE_SIZE': '50MB',  # Should convert to bytes
        }):
            config = Config()

            # Check type conversions
            assert config.get('api.timeout') == 120
            assert isinstance(config.get('api.timeout'), int)
            assert config.get('app.debug') is True
            assert isinstance(config.get('app.debug'), bool)
            # File size should be converted to bytes (50MB = 50 * 1024 * 1024)
            expected_size = 50 * 1024 * 1024
            assert config.get('logging.max_file_size') == expected_size

    def test_config_env_variable_invalid_conversion(self):
        """Test handling of invalid environment variable values."""

        with patch.dict('os.environ', {
            '{{ cookiecutter.package_name|upper }}_API_TIMEOUT': 'not_a_number',  # Invalid integer
            '{{ cookiecutter.package_name|upper }}_LOG_MAX_FILE_SIZE': 'invalid_size',  # Invalid size
        }):
            config = Config()

            # Should fallback to string values when conversion fails
            assert config.get('api.timeout') == 'not_a_number'
            assert config.get('logging.max_file_size') == 'invalid_size'

    def test_config_reload_functionality(self, sample_config_file):
        """Test configuration reload functionality."""

        config = Config(config_file=str(sample_config_file))
        original_timeout = config.get('api.timeout')

        # Modify the config file
        new_content = """
{
    "api": {
        "timeout": 999,
        "max_retries": 3,
        "base_url": "https://api.example.com"
    }
}
"""
        sample_config_file.write_text(new_content.strip())

        # Reload configuration
        config.reload()

        # Should pick up new values
        assert config.get('api.timeout') == 999
        assert config.get('api.timeout') != original_timeout

    def test_config_get_section(self):
        """Test getting entire configuration sections."""

        config = Config()

        # Get logging section
        logging_section = config.get_section('logging')
        assert isinstance(logging_section, dict)
        assert 'level' in logging_section
        assert 'console_level' in logging_section

        # Get non-existent section
        empty_section = config.get_section('non_existent')
        assert empty_section == {}

    def test_config_get_all(self):
        """Test getting the entire configuration."""

        config = Config()

        all_config = config.get_all()
        assert isinstance(all_config, dict)
        assert 'logging' in all_config
        assert 'api' in all_config
        assert 'database' in all_config
        assert 'app' in all_config

        # Verify it's a copy (modifications don't affect original)
        all_config['new_key'] = 'new_value'
        assert 'new_key' not in config.get_all()

    def test_config_dict_access(self):
        """Test dictionary-style access to config."""

        config = Config()

        # Test __getitem__
        logging_section = config['logging']
        assert isinstance(logging_section, dict)

        # Test __contains__
        assert 'logging' in config
        assert 'api' in config
        assert 'non_existent_section' not in config
