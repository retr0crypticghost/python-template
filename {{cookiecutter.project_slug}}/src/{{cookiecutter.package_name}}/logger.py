"""
Enhanced modular logger configuration for {{ cookiecutter.package_name }}.

This module provides a centralized, secure, and performant logging system
with thread safety, sensitive data filtering, and configuration integration.
"""

import json
import logging
import logging.handlers
import os
import re
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar


class SensitiveDataFilter(logging.Filter):
    """Filter to sanitize sensitive information from log records."""

    def __init__(self):
        super().__init__()
        # Compile patterns once for better performance
        self.sensitive_patterns = [
            # Key-value patterns (case insensitive)
            re.compile(r'(password\s*[:=]\s*)([^\s,\]})]+)', re.IGNORECASE),
            re.compile(r'(secret\s*[:=]\s*)([^\s,\]})]+)', re.IGNORECASE),
            re.compile(r'(token\s*[:=]\s*)([^\s,\]})]+)', re.IGNORECASE),
            re.compile(r'(api[_-]?\s*key\s*[:=]?\s*)([^\s,\]})]+)', re.IGNORECASE),
            re.compile(r'(auth\w*\s*[:=]\s*)([^\s,\]})]+)', re.IGNORECASE),
            re.compile(r'(bearer\s+)([^\s,\]})]+)', re.IGNORECASE),

            # Long alphanumeric strings that look like tokens/keys
            re.compile(r'\b[A-Za-z0-9]{32,}\b'),

            # Credit card numbers
            re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),

            # Social Security Numbers
            re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        ]

        # Sensitive field names for dictionary sanitization
        self.sensitive_keys = {
            'password', 'secret', 'token', 'key', 'auth', 'credential',
            'session', 'cookie', 'bearer', 'authorization', 'api_key',
            'access_token', 'refresh_token', 'private_key', 'cert'
        }

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter and sanitize the log record."""
        try:
            # Sanitize the message
            if hasattr(record, 'msg'):
                if record.msg is None:
                    # Handle None messages with a sanitization error
                    record.msg = "[SANITIZATION_ERROR] Message was None"
                elif isinstance(record.msg, str):
                    record.msg = self._sanitize_text(record.msg)

            # Sanitize arguments
            if record.args:
                # Handle the case where LogRecord unpacks a single dict argument
                if isinstance(record.args, dict):
                    # Convert back to tuple format expected by tests
                    sanitized_dict: dict[str, Any] = self._sanitize_dict(record.args)
                    record.args = (sanitized_dict,)
                # Handle normal case where args is a tuple
                elif isinstance(record.args, (tuple, list)):
                    sanitized_args: list[Any] = []
                    for arg in record.args:
                        if isinstance(arg, str):
                            sanitized_args.append(self._sanitize_text(arg))
                        elif isinstance(arg, dict):
                            sanitized_args.append(self._sanitize_dict(arg))
                        elif isinstance(arg, (list, tuple)):
                            sanitized_args.append(self._sanitize_sequence(arg))
                        else:
                            sanitized_args.append(arg)
                    record.args = tuple(sanitized_args)
        except Exception as e:
            # If sanitization fails, allow the log through but note the issue
            record.msg = f"[SANITIZATION_ERROR] {getattr(record, 'msg', 'Unknown message')}: {e}"

        return True

    def _sanitize_text(self, text: str) -> str:
        """Apply all sanitization patterns to text."""
        min_capture_groups = 2  # Minimum groups needed for prefix-value patterns
        for pattern in self.sensitive_patterns:
            if pattern.groups >= min_capture_groups:
                # Patterns with capture groups (keep prefix, redact value)
                text = pattern.sub(r'\1[REDACTED]', text)
            else:
                # Simple patterns (replace entire match)
                text = pattern.sub('[REDACTED]', text)
        return text

    def _sanitize_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        """Sanitize dictionary values."""
        sanitized = {}
        for key, value in data.items():
            # Check if key name suggests sensitive data
            key_lower = key.lower()
            is_sensitive_key = any(sensitive in key_lower for sensitive in self.sensitive_keys)

            if is_sensitive_key and isinstance(value, str):
                sanitized[key] = '[REDACTED]'
            elif isinstance(value, str):
                sanitized[key] = self._sanitize_text(value)
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_dict(value)
            elif isinstance(value, (list, tuple)):
                sanitized[key] = self._sanitize_sequence(value)
            else:
                sanitized[key] = value
        return sanitized

    def _sanitize_sequence(self, data):
        """Sanitize list or tuple values."""
        sanitized: list[Any] = []
        for item in data:
            if isinstance(item, str):
                sanitized.append(self._sanitize_text(item))
            elif isinstance(item, dict):
                sanitized.append(self._sanitize_dict(item))
            elif isinstance(item, (list, tuple)):
                sanitized.append(self._sanitize_sequence(item))
            else:
                sanitized.append(item)
        return type(data)(sanitized)


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to console output with security."""

    # ANSI color codes
    COLORS: ClassVar[dict[str, str]] = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        # Make a copy to avoid modifying the original record
        record_copy = logging.makeLogRecord(record.__dict__)

        # Add colors for console output
        if record_copy.levelname in self.COLORS:
            record_copy.levelname = f"{self.COLORS[record_copy.levelname]}{record_copy.levelname}{self.RESET}"

        return super().format(record_copy)


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelno,
            'level_name': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'thread': record.thread,
            'thread_name': record.threadName,
        }

        # Add exception info if present
        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)

        # Add extra fields from record
        for key, value in record.__dict__.items():
            if key not in log_obj and not key.startswith('_'):
                # Handle non-serializable values
                try:
                    json.dumps(value)  # Test if value is serializable
                    log_obj[key] = value
                except (TypeError, ValueError):
                    # Convert non-serializable values to string
                    log_obj[key] = str(value)

        return json.dumps(log_obj, default=str)


class ProjectLogger:
    """Enhanced thread-safe logger with security and performance improvements."""

    _instance = None
    _logger: logging.Logger | None = None
    _audit_logger: logging.Logger | None = None
    _lock = threading.RLock()  # Reentrant lock for nested calls
    _initialized = False

    def __new__(cls):
        """Thread-safe singleton implementation."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the logger if not already done."""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._setup_logger()
                    self._setup_audit_logger()
                    self._setup_exception_handling()
                    self._initialized = True

    def _get_config(self):
        """Get configuration with fallback."""
        try:
            from .config import get_config  # noqa: PLC0415
            return get_config()
        except ImportError:
            # Fallback configuration if config system isn't available
            return self._get_fallback_config()

    def _get_fallback_config(self):
        """Fallback configuration when config system is not available."""
        class FallbackConfig:
            def get(self, key: str, default=None):
                fallback_values = {
                    'logging.console_level': os.getenv('{{ cookiecutter.package_name|upper }}_CONSOLE_LOG_LEVEL', 'INFO'),
                    'logging.file_level': os.getenv('{{ cookiecutter.package_name|upper }}_FILE_LOG_LEVEL', 'DEBUG'),
                    'logging.file_path': os.getenv('{{ cookiecutter.package_name|upper }}_LOG_FILE_PATH', 'logs/{{ cookiecutter.package_name }}.log'),
                    'logging.max_file_size': os.getenv('{{ cookiecutter.package_name|upper }}_LOG_MAX_FILE_SIZE', '10MB'),
                    'logging.backup_count': int(os.getenv('{{ cookiecutter.package_name|upper }}_LOG_BACKUP_COUNT', '5')),
                    'logging.format': os.getenv('{{ cookiecutter.package_name|upper }}_LOG_FORMAT', 'standard'),
                    'logging.enable_json': os.getenv('{{ cookiecutter.package_name|upper }}_LOG_JSON', 'false').lower() == 'true',
                }
                return fallback_values.get(key, default)

        return FallbackConfig()

    def _setup_logger(self):
        """Set up the main logger with enhanced handlers."""
        config = self._get_config()

        # Create main logger
        self._logger = logging.getLogger('{{ cookiecutter.package_name }}')
        self._logger.setLevel(logging.DEBUG)

        # Clear any existing handlers to prevent duplicates
        self._logger.handlers.clear()

        # Create security filter
        security_filter = SensitiveDataFilter()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_level_str = config.get('logging.console_level', 'INFO')
        console_level = str(console_level_str or 'INFO').upper()
        console_handler.setLevel(getattr(logging, console_level, logging.INFO))
        console_handler.addFilter(security_filter)

        console_formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)

        # File handler with rotation
        log_file_path = config.get('logging.file_path', 'logs/{{ cookiecutter.package_name }}.log')
        log_file = Path(str(log_file_path or 'logs/{{ cookiecutter.package_name }}.log'))
        log_file.parent.mkdir(parents=True, exist_ok=True)

        max_size_str = config.get('logging.max_file_size', '10MB')
        max_bytes = self._parse_file_size(str(max_size_str or '10MB'))
        backup_count_val = config.get('logging.backup_count', 5)
        backup_count = int(backup_count_val or 5)

        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )

        file_level_str = config.get('logging.file_level', 'DEBUG')
        file_level = str(file_level_str or 'DEBUG').upper()
        file_handler.setLevel(getattr(logging, file_level, logging.DEBUG))
        file_handler.addFilter(security_filter)

        # Choose formatter based on configuration
        enable_json = config.get('logging.enable_json', False)
        if bool(enable_json):
            file_formatter: logging.Formatter = JSONFormatter()
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        file_handler.setFormatter(file_formatter)

        # Error file handler
        error_file = log_file.parent / f'errors_{log_file.name}'
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.addFilter(security_filter)
        error_handler.setFormatter(file_formatter)

        # Add all handlers
        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)
        self._logger.addHandler(error_handler)

        # Prevent propagation to root logger
        self._logger.propagate = False

    def _setup_audit_logger(self):
        """Set up separate audit logger for security events."""
        self._audit_logger = logging.getLogger('{{ cookiecutter.package_name }}.audit')
        self._audit_logger.setLevel(logging.INFO)

        # Clear existing handlers
        self._audit_logger.handlers.clear()

        # Audit log file with rotation
        audit_file = Path('logs/audit.log')
        audit_file.parent.mkdir(parents=True, exist_ok=True)

        audit_handler = logging.handlers.RotatingFileHandler(
            audit_file,
            maxBytes=50*1024*1024,  # 50MB
            backupCount=10,
            encoding='utf-8'
        )

        # Audit logs use JSON format for structured analysis
        audit_formatter = JSONFormatter()
        audit_handler.setFormatter(audit_formatter)

        self._audit_logger.addHandler(audit_handler)

        # Audit logs should not propagate to prevent duplication
        self._audit_logger.propagate = False

    def _setup_exception_handling(self):
        """Set up global exception logging."""
        def exception_handler(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            if self._logger:
                self._logger.critical(
                    "Uncaught exception",
                    exc_info=(exc_type, exc_value, exc_traceback)
                )

        sys.excepthook = exception_handler

    def _parse_file_size(self, size_str: str) -> int:
        """Parse file size string to bytes."""
        if isinstance(size_str, int):
            return size_str

        size_str = str(size_str).upper()
        multipliers = {'KB': 1024, 'MB': 1024**2, 'GB': 1024**3}

        for suffix, multiplier in multipliers.items():
            if size_str.endswith(suffix):
                try:
                    return int(float(size_str[:-len(suffix)]) * multiplier)
                except ValueError:
                    break

        try:
            return int(float(size_str))
        except ValueError:
            return 10 * 1024 * 1024  # Default 10MB

    def get_logger(self, name: str | None = None) -> logging.Logger:
        """Get a logger instance."""
        if not self._logger:
            raise RuntimeError("Logger not initialized")

        if name is None:
            return self._logger
        return self._logger.getChild(name)

    def get_audit_logger(self) -> logging.Logger:
        """Get the audit logger for security events."""
        if not self._audit_logger:
            raise RuntimeError("Audit logger not initialized")
        return self._audit_logger

    def log_security_event(self, event_type: str, details: dict[str, Any], level: str = 'INFO'):
        """Log a security event to the audit log."""
        if self._audit_logger:
            audit_data = {
                'event_type': event_type,
                'timestamp': datetime.utcnow().isoformat(),
                'details': details
            }

            log_level = getattr(logging, level.upper(), logging.INFO)
            self._audit_logger.log(log_level, json.dumps(audit_data))

    def update_log_levels(self, console_level: str | None = None, file_level: str | None = None):
        """Update log levels dynamically."""
        if not self._logger:
            return

        with self._lock:
            for handler in self._logger.handlers:
                if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                    if console_level:
                        handler.setLevel(getattr(logging, console_level.upper(), logging.INFO))
                elif isinstance(handler, logging.handlers.RotatingFileHandler):
                    if file_level and 'error' not in str(handler.baseFilename):
                        handler.setLevel(getattr(logging, file_level.upper(), logging.DEBUG))


# Global logger instance
_{{ cookiecutter.package_name }}_logger = ProjectLogger()


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Get a logger instance for use throughout the project.

    Args:
        name: Optional name for the logger. Typically use __name__ or module name.

    Returns:
        logging.Logger: Configured logger instance.

    Example:
        >>> from logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("This is an info message")
        >>> logger.error("This is an error message")
    """
    return _{{ cookiecutter.package_name }}_logger.get_logger(name)


def get_audit_logger() -> logging.Logger:
    """Get the audit logger for security events."""
    return _{{ cookiecutter.package_name }}_logger.get_audit_logger()


def log_security_event(event_type: str, details: dict[str, Any], level: str = 'INFO'):
    """Log a security event."""
    _{{ cookiecutter.package_name }}_logger.log_security_event(event_type, details, level)


def set_log_level(console_level: str | None = None, file_level: str | None = None):
    """
    Set log levels dynamically.

    Args:
        console_level: Console log level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
                      If called with just one argument (for backward compatibility),
                      it sets the console level
        file_level: File log level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """
    # Backward compatibility: if called with single string argument
    if isinstance(console_level, str) and file_level is None:
        level = console_level.upper()
        if not hasattr(logging, level):
            raise ValueError(f'Invalid log level: {console_level}')
        _{{ cookiecutter.package_name }}_logger.update_log_levels(console_level=level)
    else:
        _{{ cookiecutter.package_name }}_logger.update_log_levels(console_level, file_level)


# Enhanced convenience functions with lazy evaluation
def debug(message: str, *args, **kwargs):
    """Log a debug message with lazy evaluation."""
    logger = _{{ cookiecutter.package_name }}_logger.get_logger()
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(message, *args, **kwargs)


def info(message: str, *args, **kwargs):
    """Log an info message."""
    _{{ cookiecutter.package_name }}_logger.get_logger().info(message, *args, **kwargs)


def warning(message: str, *args, **kwargs):
    """Log a warning message."""
    _{{ cookiecutter.package_name }}_logger.get_logger().warning(message, *args, **kwargs)


def error(message: str, *args, **kwargs):
    """Log an error message."""
    _{{ cookiecutter.package_name }}_logger.get_logger().error(message, *args, **kwargs)


def critical(message: str, *args, **kwargs):
    """Log a critical message."""
    _{{ cookiecutter.package_name }}_logger.get_logger().critical(message, *args, **kwargs)


if __name__ == "__main__":
    # Test the logger
    logger = get_logger(__name__)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Test security filtering
    logger.info("User logged in with password=secret123 and token=abc123def456")
    logger.info("API key: sk_test_1234567890abcdef")

    # Test audit logging
    log_security_event("login_attempt", {"user": "test", "ip": "192.168.1.1", "success": True})
    logger.error("This is an error message")
    logger.critical("This is a critical message")
