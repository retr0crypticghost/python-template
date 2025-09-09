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


def cleanup_project_type():
    """Handle project type specific cleanup."""
    project_type = "{{ cookiecutter.project_type }}"

    if project_type == "library":
        # Libraries don't need run scripts or CLI modules
        run_script = f"run_{{ cookiecutter.project_slug }}.py"
        remove_file(run_script)

        # Remove CLI module for library projects
        cli_module = "src/{{ cookiecutter.package_name }}/cli.py"
        remove_file(cli_module)
        
        # Remove CLI tests
        remove_file("tests/test_cli.py")

        print("✅ Library project configured - removed CLI components")

    elif project_type == "cli-application":
        # CLI apps keep the run script and CLI module
        print("✅ CLI application project configured - kept CLI components")

    else:
        print(f"⚠️  Unknown project type: {project_type}")


def cleanup_docs():
    """Handle documentation cleanup based on docs option."""
    docs_enabled = "{{ cookiecutter.docs }}" == "y"
    
    if not docs_enabled:
        remove_file("mkdocs.yml")
        remove_directory("docs")
        
        # Remove docs workflow
        remove_file(".github/workflows/docs.yml")
        
        print("✅ Documentation disabled - removed MkDocs files")
    else:
        print("✅ Documentation enabled - kept MkDocs files")


def cleanup_typed_config():
    """Handle typed config cleanup."""
    typed_config_enabled = "{{ cookiecutter.typed_config }}" == "y"
    
    if not typed_config_enabled:
        # Remove Pydantic settings file if it exists
        remove_file("src/{{ cookiecutter.package_name }}/settings.py")
        print("✅ Typed config disabled - using standard config")
    else:
        print("✅ Typed config enabled - Pydantic settings available")


def cleanup_sbom():
    """Handle SBOM workflow cleanup."""
    sbom_enabled = "{{ cookiecutter.sbom }}" == "y"
    
    if not sbom_enabled:
        remove_file(".github/workflows/sbom.yml")
        print("✅ SBOM generation disabled - removed workflow")
    else:
        print("✅ SBOM generation enabled - workflow available")


def cleanup_versioning():
    """Handle versioning cleanup based on versioning option."""
    versioning = "{{ cookiecutter.versioning }}"
    
    if versioning == "manual":
        # Remove versioning files for manual versioning
        remove_file("_version.py")  # setuptools-scm version file
        print("✅ Manual versioning configured")
    elif versioning == "setuptools-scm":
        print("✅ setuptools-scm versioning configured")
    elif versioning == "hatch":
        print("✅ Hatch versioning configured")


def main():
    """Main post-generation logic."""
    print("🔧 Configuring generated project...")

    # Handle different project types
    cleanup_project_type()
    
    # Handle optional features
    cleanup_docs()
    cleanup_typed_config()
    cleanup_sbom()
    cleanup_versioning()

    print("✅ Project generation completed successfully!")


if __name__ == "__main__":
    main()
