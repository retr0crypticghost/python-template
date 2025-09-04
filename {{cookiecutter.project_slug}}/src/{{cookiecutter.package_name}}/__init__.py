"""
{{ cookiecutter.package_name }} package - A modular Python application framework.

This package provides centralized logging, hierarchical configuration management,
and environment variable validation for Python applications.
"""

__version__ = "0.1.0"

from .config import get_config, reload_config
from .core import App, main
from .logger import (
    critical,
    debug,
    error,
    get_logger,
    info,
    warning,
)

__version__ = "0.1.0"
__author__ = "{{ cookiecutter.author_name }}"

__all__ = [
    "App",
    "critical",
    "debug",
    "error",
    "get_config",
    "get_logger",
    "info",
    "main",
    "reload_config",
    "warning",
]
