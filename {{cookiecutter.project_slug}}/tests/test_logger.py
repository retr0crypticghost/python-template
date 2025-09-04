"""
Tests for the logger module.
"""

import json
import logging
import sys
from unittest.mock import MagicMock, patch

import pytest

from {{ cookiecutter.package_name }}.logger import (
    ColoredFormatter,
    JSONFormatter,
    ProjectLogger,
    SensitiveDataFilter,
    get_audit_logger,
    get_logger,
    log_security_event,
    set_log_level,
)


class TestSensitiveDataFilter:
    """Test cases for the SensitiveDataFilter class."""

    def test_filter_initialization(self):
        """Test that SensitiveDataFilter initializes correctly."""
        filter_obj = SensitiveDataFilter()
        assert filter_obj is not None
        assert hasattr(filter_obj, 'sensitive_patterns')
        assert hasattr(filter_obj, 'sensitive_keys')

    def test_sanitize_password_in_text(self):
        """Test sanitization of password in text."""
        filter_obj = SensitiveDataFilter()

        # Create a mock log record
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="User logged in with password=secret123",
            args=(),
            exc_info=None
        )

        filter_obj.filter(record)
        assert "password=[REDACTED]" in record.msg
        assert "secret123" not in record.msg

    def test_sanitize_api_key_in_text(self):
        """Test sanitization of API key in text."""
        filter_obj = SensitiveDataFilter()

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="API key: sk_test_1234567890abcdef",
            args=(),
            exc_info=None
        )

        filter_obj.filter(record)
        assert "[REDACTED]" in record.msg
        assert "sk_test_1234567890abcdef" not in record.msg

    def test_sanitize_dict_with_sensitive_keys(self):
        """Test sanitization of dictionary with sensitive keys."""
        filter_obj = SensitiveDataFilter()

        sensitive_data = {
            "username": "john",
            "password": "secret123",
            "api_key": "abc123def456",
            "normal_data": "public_info"
        }

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="User data: %s",
            args=(sensitive_data,),
            exc_info=None
        )

        filter_obj.filter(record)
        sanitized_dict = record.args[0]

        assert sanitized_dict["username"] == "john"
        assert sanitized_dict["password"] == "[REDACTED]"
        assert sanitized_dict["api_key"] == "[REDACTED]"
        assert sanitized_dict["normal_data"] == "public_info"

    def test_sanitize_nested_dict(self):
        """Test sanitization of nested dictionaries."""
        filter_obj = SensitiveDataFilter()

        nested_data = {
            "user": {
                "name": "john",
                "credentials": {
                    "password": "secret123",
                    "token": "abc123"
                }
            }
        }

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Nested data: %s",
            args=(nested_data,),
            exc_info=None
        )

        filter_obj.filter(record)
        sanitized_dict = record.args[0]

        assert sanitized_dict["user"]["name"] == "john"
        assert sanitized_dict["user"]["credentials"]["password"] == "[REDACTED]"
        assert sanitized_dict["user"]["credentials"]["token"] == "[REDACTED]"

    def test_sanitize_list_with_sensitive_data(self):
        """Test sanitization of lists containing sensitive data."""
        filter_obj = SensitiveDataFilter()

        list_data = [
            "normal_item",
            {"password": "secret123"},
            "password=secret456"
        ]

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="List data: %s",
            args=(list_data,),
            exc_info=None
        )

        filter_obj.filter(record)
        sanitized_list = record.args[0]

        assert sanitized_list[0] == "normal_item"
        assert sanitized_list[1]["password"] == "[REDACTED]"
        assert "password=[REDACTED]" in sanitized_list[2]

    def test_filter_exception_handling(self):
        """Test that filter handles exceptions gracefully."""
        filter_obj = SensitiveDataFilter()

        # Create a record with problematic data that could cause exceptions
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg=None,  # This could cause issues
            args=(),
            exc_info=None
        )

        # Should not raise exception
        result = filter_obj.filter(record)
        assert result is True
        assert "[SANITIZATION_ERROR]" in record.msg


class TestColoredFormatter:
    """Test cases for the ColoredFormatter class."""

    def test_colored_formatter_initialization(self):
        """Test that ColoredFormatter initializes correctly."""
        formatter = ColoredFormatter()
        assert formatter is not None
        assert hasattr(formatter, 'COLORS')
        assert hasattr(formatter, 'RESET')

    def test_format_with_colors(self):
        """Test formatting with colors."""
        formatter = ColoredFormatter('%(levelname)s - %(message)s')

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="Test error message",
            args=(),
            exc_info=None
        )

        formatted = formatter.format(record)
        # Should contain ANSI color codes for ERROR level
        assert '\033[31m' in formatted  # Red color for ERROR
        assert '\033[0m' in formatted   # Reset code
        assert "Test error message" in formatted


class TestJSONFormatter:
    """Test cases for the JSONFormatter class."""

    def test_json_formatter_initialization(self):
        """Test that JSONFormatter initializes correctly."""
        formatter = JSONFormatter()
        assert formatter is not None

    def test_format_basic_record(self):
        """Test formatting a basic log record to JSON."""
        formatter = JSONFormatter()

        record = logging.LogRecord(
            name="test.module",
            level=logging.INFO,
            pathname="/path/to/file.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None
        )
        record.funcName = "test_function"
        record.thread = 12345
        record.threadName = "MainThread"
        record.module = "test_module"

        formatted = formatter.format(record)
        parsed = json.loads(formatted)

        assert parsed["level"] == logging.INFO
        assert parsed["level_name"] == "INFO"
        assert parsed["logger"] == "test.module"
        assert parsed["message"] == "Test message"
        assert parsed["module"] == "test_module"
        assert parsed["function"] == "test_function"
        assert parsed["line"] == 42
        assert parsed["thread"] == 12345
        assert parsed["thread_name"] == "MainThread"
        assert "timestamp" in parsed

    def test_format_with_exception(self):
        """Test formatting a record with exception info."""
        formatter = JSONFormatter()

        try:
            raise ValueError("Test exception")
        except ValueError:
            exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="Error occurred",
            args=(),
            exc_info=exc_info
        )

        formatted = formatter.format(record)
        parsed = json.loads(formatted)

        assert "exception" in parsed
        assert "ValueError" in parsed["exception"]
        assert "Test exception" in parsed["exception"]


class TestMainLogger:
    """Test cases for the main logger functionality."""

    def test_get_logger(self):
        """Test getting a logger instance."""
        logger = get_logger("test.module")
        assert logger is not None
        assert isinstance(logger, logging.Logger)

    def test_get_logger_without_name(self):
        """Test getting logger without specifying name."""
        logger = get_logger()
        assert logger is not None
        assert isinstance(logger, logging.Logger)

    def test_get_audit_logger(self):
        """Test getting the audit logger."""
        audit_logger = get_audit_logger()
        assert audit_logger is not None
        assert isinstance(audit_logger, logging.Logger)
        assert "audit" in audit_logger.name

    def test_log_security_event(self):
        """Test logging a security event."""
        # This should not raise any exceptions
        log_security_event(
            "test_event",
            {"user": "test_user", "action": "login"},
            "INFO"
        )

    def test_set_log_level(self):
        """Test setting log level."""
        # This should not raise any exceptions
        set_log_level("DEBUG")
        set_log_level("INFO", "DEBUG")

    def test_set_invalid_log_level(self):
        """Test setting an invalid log level."""
        with pytest.raises(ValueError, match="Invalid log level"):
            set_log_level("INVALID_LEVEL")

    @patch('{{ cookiecutter.package_name }}.logger._{{ cookiecutter.package_name }}_logger')
    def test_logger_singleton(self, mock_logger_instance):
        """Test that logger uses singleton pattern."""
        mock_logger_instance.get_logger = MagicMock()

        # Multiple calls should return the same instance
        get_logger("test1")
        get_logger("test2")

        # The underlying logger instance should be called to get loggers
        assert mock_logger_instance.get_logger.call_count >= 2


class TestLoggerConfiguration:
    """Test cases for logger configuration."""

    def test_logger_initialization_with_fallback_config(self, temp_dir):
        """Test logger initialization when config system is not available."""
        # This is tested implicitly by the above tests since they work
        # without a full config system setup
        logger = get_logger("test")
        assert logger is not None

    def test_parse_file_size(self):
        """Test file size parsing functionality."""
        logger_instance = ProjectLogger()

        # Test various size formats
        assert logger_instance._parse_file_size("1024") == 1024
        assert logger_instance._parse_file_size("1KB") == 1024
        assert logger_instance._parse_file_size("1MB") == 1024 * 1024
        assert logger_instance._parse_file_size("1GB") == 1024 * 1024 * 1024
        assert logger_instance._parse_file_size("10.5MB") == int(10.5 * 1024 * 1024)

        # Test invalid formats (should return default)
        default_size = 10 * 1024 * 1024  # 10MB default
        assert logger_instance._parse_file_size("invalid") == default_size
        assert logger_instance._parse_file_size("") == default_size

    def test_logger_with_temp_directory(self, temp_dir):
        """Test logger creation with temporary directory for logs."""
        with patch.dict("os.environ", {"{{ cookiecutter.package_name | upper }}_LOG_FILE_PATH": str(temp_dir / "test.log")}):
            logger = get_logger("test.with.temp")
            assert logger is not None

            # Test that we can log messages
            logger.info("Test log message")
            logger.error("Test error message")


# Integration tests
class TestLoggerIntegration:
    """Integration tests for the complete logger functionality."""

    def test_complete_logging_workflow(self, temp_dir):
        """Test a complete logging workflow with file output."""
        log_file = temp_dir / "integration_test.log"

        with patch.dict("os.environ", {
            "{{ cookiecutter.package_name | upper }}_LOG_FILE_PATH": str(log_file),
            "{{ cookiecutter.package_name | upper }}_CONSOLE_LOG_LEVEL": "WARNING",
            "{{ cookiecutter.package_name | upper }}_FILE_LOG_LEVEL": "DEBUG"
        }):
            # Get logger and log various levels
            logger = get_logger("integration.test")

            logger.debug("Debug message with sensitive data: password=secret123")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")

            # Test audit logging
            log_security_event("integration_test", {
                "test": True,
                "user_id": 12345,
                "password": "should_be_redacted"
            })

    def test_exception_logging(self):
        """Test that exceptions are properly logged."""
        logger = get_logger("exception.test")

        try:
            raise RuntimeError("Test exception for logging")
        except RuntimeError:
            logger.exception("Exception occurred during test")

    def test_logger_performance(self):
        """Basic performance test for logger."""
        logger = get_logger("performance.test")

        # Log many messages quickly - should not fail
        for i in range(100):
            logger.info(f"Performance test message {i}")
