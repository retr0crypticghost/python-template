# Contributing to retr0crypticghost's Python Template

Thank you for considering contributing to this Python project template! This document provides guidelines and information for contributors.

## Philosophy

This template follows a practical, experience-driven approach:
- **Features are added when actually needed**, not because they're trendy
- **Real-world usage drives decisions**, not theoretical best practices
- **Simplicity over complexity** - the template should be easy to understand and modify
- **Opinionated but flexible** - strong defaults that can be easily customized

## Types of Contributions

### 🐛 Bug Reports
- Use the GitHub issue template
- Include clear reproduction steps
- Mention which project type (library/CLI) is affected
- Include your environment details (Python version, OS, etc.)

### 💡 Feature Requests
- Explain the real-world use case
- Describe how it fits with existing features
- Consider if it belongs in the template or should be project-specific

### 📝 Documentation
- Improve existing documentation clarity
- Add missing examples or use cases
- Fix typos and formatting issues

### 🔧 Code Changes
- Follow the existing code style and patterns
- Test with both library and CLI project types
- Update documentation if needed
- Keep changes focused and atomic

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/python-template.git
   cd python-template
   ```

2. **Test template generation**
   ```bash
   # Test library generation
   cookiecutter . --no-input project_type=library

   # Test CLI generation
   cookiecutter . --no-input project_type=cli-application

   # Clean up test projects
   rm -rf my-python-project
   ```

3. **Validate generated projects**
   ```bash
   cd test-project
   pip install -e ".[dev]"
   pytest
   ```

## Testing Guidelines

### Template Testing
- Always test both project types (library and CLI)
- Verify generated projects install correctly
- Check that all template variables render properly
- Test with different input values

### Generated Project Testing
- Ensure tests pass in generated projects
- Verify configuration loading works
- Test logging functionality
- Check CLI features (for CLI projects)

## Code Style

- Follow existing patterns in the template
- Use meaningful variable names in cookiecutter.json
- Keep template files focused and readable
- Comment complex Jinja2 logic

## Commit Messages

Use clear, descriptive commit messages:
- `feat: add new feature`
- `fix: resolve issue with X`
- `docs: improve README examples`
- `refactor: simplify configuration loading`
- `test: add validation for CLI projects`

## Pull Request Process

1. **Create a focused PR** - one feature or fix per PR
2. **Update documentation** if your changes affect usage
3. **Test thoroughly** with both project types
4. **Write a clear description** of what changed and why
5. **Be responsive** to feedback and questions

## Questions?

- Open an issue for questions about contributing
- Check existing issues and PRs for similar discussions
- Feel free to propose changes to these guidelines

## Recognition

All contributors will be recognized in the project. Thank you for helping make this template better for everyone!
