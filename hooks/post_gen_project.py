#!/usr/bin/env python3
"""
Post-generation hook for python-template cookiecutter.

This script runs after the project is generated and customizes
the project based on the selected options.
"""

import os
import shutil
from pathlib import Path

PROJECT_DIRECTORY = Path.cwd()


def remove_file(filepath):
    """Remove a file if it exists."""
    file_path = PROJECT_DIRECTORY / filepath
    if file_path.exists():
        file_path.unlink()
        print(f"Removed {filepath}")


def remove_directory(dirpath):
    """Remove a directory if it exists."""
    dir_path = PROJECT_DIRECTORY / dirpath
    if dir_path.exists():
        shutil.rmtree(dir_path)
        print(f"Removed {dirpath}")


def main():
    """Main post-generation logic."""

    project_type = "{{ cookiecutter.project_type }}"

    if project_type == "library":
        # Libraries don't need run scripts or CLI modules
        run_script = f"run_{{ cookiecutter.project_slug }}.py"
        remove_file(run_script)

        # Remove CLI module for library projects
        cli_module = "src/{{ cookiecutter.package_name }}/cli.py"
        remove_file(cli_module)

        print("✅ Library project configured - removed CLI components")

    elif project_type == "cli-application":
        # CLI apps keep the run script and CLI module
        print("✅ CLI application project configured - kept CLI components")

    else:
        print(f"⚠️  Unknown project type: {project_type}")

    print("✅ Project generation completed successfully!")


if __name__ == "__main__":
    main()
