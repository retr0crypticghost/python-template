# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Features

- **🔍 Professional Logging**: Security-aware logging with sensitive data filtering
- **🔒 Audit Trail**: Security events and compliance logging
- **⚙️ Hierarchical Configuration**: YAML config files with environment variable overrides
- **🔍 Environment Validation**: Automatic checking of required vs optional environment variables
- **🧵 Thread Safety**: Safe concurrent operations throughout
- **🎨 Rich Output**: Colored console logs with structured JSON for production
- **📁 Best Practices**: Python packaging standards with src/ layout
- **🧪 Comprehensive Testing**: Full test suite with security and performance tests
{%- if cookiecutter.project_type == "cli-application" %}
- **⚡ Professional CLI**: Rich command-line interface with Click framework
- **🗂️ Shell Completion**: Auto-completion for bash, zsh, fish, and PowerShell
- **📖 Man Page Generation**: Automatic documentation for system integration
{%- endif %}

## Quick Start

### Installation

```bash
pip install {{cookiecutter.project_slug}}
```

{%- if cookiecutter.project_type == "cli-application" %}

### Command Line Usage

```bash
# Get help
{{cookiecutter.package_name}} --help

# Basic usage examples
{{cookiecutter.package_name}} status
{{cookiecutter.package_name}} hello "World"
```

{%- endif %}

### Python Usage

```python
import {{cookiecutter.package_name}}
from {{cookiecutter.package_name}} import get_logger, get_config

# Get logger with automatic security filtering
logger = get_logger(__name__)
logger.info("Application started")

# Access configuration
config = get_config()
debug_mode = config.get('app.debug', False)
```

## Configuration

{{cookiecutter.project_name}} uses a hierarchical configuration system:

1. **Default values** (built into the application)
2. **Configuration file** (`config.yaml` in the project root)
3. **Environment variables** (highest priority)

### Configuration File

Create a `config.yaml` file in your project root:

```yaml
app:
  name: {{cookiecutter.package_name}}
  debug: false

logging:
  level: INFO
  console_level: INFO
  file_level: DEBUG
  file_path: logs/{{cookiecutter.package_name}}.log

# Add your custom configuration here
```

### Environment Variables

Override any configuration value with environment variables:

```bash
export {{cookiecutter.package_name.upper()}}_APP_DEBUG=true
export {{cookiecutter.package_name.upper()}}_LOGGING_LEVEL=DEBUG
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}.git
cd {{cookiecutter.project_slug}}

# Install development dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov={{cookiecutter.package_name}}

# Run specific test categories
pytest tests/test_config.py
pytest tests/test_security.py
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy src/

# Run all pre-commit hooks
pre-commit run --all-files
```

## Project Structure

```
{{cookiecutter.project_slug}}/
├── src/{{cookiecutter.package_name}}/     # Main package
│   ├── __init__.py           # Package exports
│   ├── config.py             # Configuration management
│   ├── core.py               # Application core logic
│   └── logger.py             # Professional logging system
├── tests/                    # Comprehensive test suite
│   ├── test_config.py        # Configuration tests
│   └── test_core.py          # Core functionality tests
├── docs/                     # Documentation source
├── config.yaml               # Configuration template
├── pyproject.toml            # Project configuration
└── README.md                 # Project documentation
```

## License

{% if cookiecutter.license != 'Private' -%}
This project is licensed under the {{cookiecutter.license}} License - see the LICENSE file for details.
{% else -%}
This project is private and proprietary.
{% endif %}

## Contributing

See [Contributing Guide](contributing.md) for development guidelines.

## Author

**{{cookiecutter.author_name}}** - {{cookiecutter.author_email}}

---

*Generated from the [Python Professional Template](https://github.com/{{cookiecutter.github_username}}/python-template) - Practical Python project foundations*
