# Contributing to {{cookiecutter.project_name}}

Thank you for considering contributing to {{cookiecutter.project_name}}! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python {{cookiecutter.python_version}}+
- Git

### Setup Instructions

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}.git
   cd {{cookiecutter.project_slug}}
   ```

2. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Setup pre-commit hooks**
   ```bash
   pre-commit install
   ```

4. **Verify installation**
   ```bash
   # Run tests to ensure everything works
   pytest

   # Run linting
   ruff check .

   # Run type checking
   mypy src/
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the project style
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run all tests
   pytest

   # Run with coverage
   pytest --cov={{cookiecutter.package_name}}

   # Run linting and formatting
   ruff check .
   ruff format .

   # Run type checking
   mypy src/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Then create a Pull Request on GitHub
   ```

## Code Style

### Python Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for code formatting and linting:

- **Line length**: 100 characters
- **Quote style**: Double quotes
- **Import sorting**: Automatic with Ruff
- **Code formatting**: Automatic with `ruff format`

### Commit Message Format

We use conventional commits:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```bash
git commit -m "feat: add new configuration loader"
git commit -m "fix: handle missing config file gracefully"
git commit -m "docs: update installation instructions"
```

## Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_should_load_config_from_file`
- Test both success and failure cases
- Mock external dependencies
- Aim for high test coverage (>80%)

### Test Categories

```bash
# Unit tests
pytest tests/test_config.py

# Integration tests
pytest tests/test_integration.py

# Security tests
pytest tests/test_security.py

# Performance tests
pytest tests/test_performance.py
```

### Test Data

- Use fixtures for test data
- Keep test data minimal and focused
- Don't commit sensitive test data

## Documentation

### Code Documentation

- Use docstrings for all public functions and classes
- Follow Google style docstrings
- Include examples in docstrings when helpful

```python
def load_config(file_path: str) -> dict:
    """Load configuration from a YAML file.

    Args:
        file_path: Path to the YAML configuration file.

    Returns:
        Dictionary containing the configuration data.

    Raises:
        FileNotFoundError: If the configuration file doesn't exist.
        yaml.YAMLError: If the file contains invalid YAML.

    Example:
        >>> config = load_config("config.yaml")
        >>> print(config["app"]["name"])
    """
```

### Documentation Site

This project uses MkDocs Material for documentation:

- Documentation source is in `docs/`
- Build locally: `mkdocs serve`
- Preview at: http://localhost:8000

## Security

### Security Considerations

- Never commit secrets or API keys
- Use environment variables for sensitive configuration
- Review the [Security Policy](../SECURITY.md) for reporting vulnerabilities
- Test security features thoroughly

### Security Testing

```bash
# Run security-specific tests
pytest tests/test_security.py

# Check dependencies for vulnerabilities
safety check

# Run security linting
bandit -r src/
```

## Performance

### Performance Considerations

- Profile code for performance bottlenecks
- Avoid premature optimization
- Consider memory usage for large datasets
- Test with realistic data sizes

### Performance Testing

```bash
# Run performance tests
pytest tests/test_performance.py

# Profile code
python -m cProfile -o profile.stats your_script.py
```

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- `MAJOR.MINOR.PATCH`
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

### Creating Releases

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create and push tag: `git tag v1.0.0`
4. GitHub Actions will automatically build and publish to PyPI

## Getting Help

### Communication

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: Contact {{cookiecutter.author_email}} for sensitive matters

### Resources

- [Project Documentation](https://{{cookiecutter.github_username}}.github.io/{{cookiecutter.project_slug}})
- [Python Packaging Guide](https://packaging.python.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)

## Recognition

Contributors will be recognized in:

- GitHub Contributors list
- CHANGELOG.md for significant contributions
- Documentation acknowledgments

Thank you for contributing to {{cookiecutter.project_name}}!
