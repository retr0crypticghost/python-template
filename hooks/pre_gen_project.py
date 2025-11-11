#!/usr/bin/env python3
"""
Pre-generation hook for python-template cookiecutter.

This script runs before the project is generated and validates
the user inputs, ensuring they meet requirements.
"""

import re
import sys
from pathlib import Path


def validate_package_name(package_name: str) -> bool:
    """
    Validate that package_name is a valid Python identifier.
    
    Args:
        package_name: The package name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if it's a valid Python identifier
    if not package_name.isidentifier():
        return False
    
    # Check for Python keywords
    import keyword
    if keyword.iskeyword(package_name):
        return False
        
    # Check for reserved names
    reserved_names = {
        'test', 'tests', 'lib', 'src', 'docs', 'examples', 'example',
        'setup', 'build', 'dist', 'egg-info', '__pycache__'
    }
    if package_name.lower() in reserved_names:
        return False
    
    return True


def normalize_project_slug(project_slug: str) -> str:
    """
    Normalize project slug to follow best practices.
    
    Args:
        project_slug: The project slug to normalize
        
    Returns:
        str: Normalized project slug
    """
    # Convert to lowercase
    slug = project_slug.lower()
    
    # Replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)
    
    # Remove invalid characters
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    
    # Remove leading/trailing hyphens and collapse multiple hyphens
    slug = re.sub(r'-+', '-', slug).strip('-')
    
    return slug


def validate_inputs():
    """Validate all cookiecutter inputs."""
    errors = []
    
    # Get cookiecutter variables
    package_name = "{{ cookiecutter.package_name }}"
    project_slug = "{{ cookiecutter.project_slug }}"
    project_type = "{{ cookiecutter.project_type }}"
    package_manager = "{{ cookiecutter.package_manager }}"
    python_version = "{{ cookiecutter.python_version }}"
    
    # Validate package name
    if not validate_package_name(package_name):
        errors.append(f"❌ Invalid package_name '{package_name}': Must be a valid Python identifier")
        errors.append("   - Cannot contain spaces, hyphens, or special characters")
        errors.append("   - Cannot be a Python keyword")
        errors.append("   - Cannot be a reserved name (test, tests, lib, src, etc.)")
        
    # Validate project type
    valid_project_types = ["library", "cli-application"]
    if project_type not in valid_project_types:
        errors.append(f"❌ Invalid project_type '{project_type}': Must be one of {valid_project_types}")
    
    # Validate package manager
    valid_package_managers = ["pip", "uv", "hatch"]
    if package_manager not in valid_package_managers:
        errors.append(f"❌ Invalid package_manager '{package_manager}': Must be one of {valid_package_managers}")
    
    # Validate Python version format
    try:
        version_parts = python_version.split('.')
        if len(version_parts) != 2:
            raise ValueError("Invalid format")
        major, minor = int(version_parts[0]), int(version_parts[1])
        if major != 3 or minor < 11:
            errors.append(f"❌ Invalid python_version '{python_version}': Must be 3.11 or higher")
    except ValueError:
        errors.append(f"❌ Invalid python_version '{python_version}': Must be in format 'X.Y' (e.g., '3.11')")
    
    # Check for potential slug issues (warn but don't fail)
    normalized_slug = normalize_project_slug(project_slug)
    if project_slug != normalized_slug:
        print(f"⚠️  Project slug '{project_slug}' would be normalized to '{normalized_slug}'")
        print("   Consider using the normalized version for better compatibility")
    
    if errors:
        print("🛑 Cookiecutter validation failed:")
        print()
        for error in errors:
            print(error)
        print()
        print("💡 Tips:")
        print("   - Use underscores for package_name: my_package")  
        print("   - Use hyphens for project_slug: my-project")
        print("   - Choose from supported project types: library, cli-application")
        print("   - Choose from supported package managers: pip, uv, hatch")
        sys.exit(1)
    
    print("✅ Input validation passed!")


def main():
    """Main pre-generation logic."""
    print("🔍 Validating cookiecutter inputs...")
    validate_inputs()


if __name__ == "__main__":
    main()