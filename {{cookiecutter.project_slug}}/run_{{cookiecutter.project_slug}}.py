#!/usr/bin/env python3
"""
{{ cookiecutter.project_name }} - {{ cookiecutter.project_description }}

{%- if cookiecutter.project_type == "cli-application" %}
Command-line interface entry point for {{ cookiecutter.project_name }}.
{%- else %}
Main application entry point for {{ cookiecutter.project_name }}.
{%- endif %}
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

{%- if cookiecutter.project_type == "cli-application" %}
from {{ cookiecutter.package_name }}.cli import main  # noqa: E402, I001
{%- else %}
from {{ cookiecutter.package_name }}.core import main
{%- endif %}


if __name__ == "__main__":
    main()
