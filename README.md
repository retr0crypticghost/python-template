# Python Professional Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Cookiecutter](https://img.shields.io/badge/cookiecutter-template-blue.svg)](https://github.com/cookiecutter/cookiecutter)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Security: OpenSSF Scorecard](https://img.shields.io/badge/OpenSSF-Scorecard-blue)](https://github.com/ossf/scorecard)

**Production-ready project scaffolding with security and quality foundations**

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for Python projects that includes professional patterns I've found useful: security-conscious logging, hierarchical configuration, and modern development practices.

> **🎯 Goal**: Skip the repetitive setup work. Get Python projects with good security and testing practices built-in.

> **🏗️ What This Provides**: A solid foundation with opinionated choices about logging, configuration, and CLI tooling. More comprehensive than basic templates, but not a complete framework.

> **📝 Approach**: Features are added based on real project needs, not theoretical completeness. Patterns evolve as I learn better ways to structure Python applications.

## What This Template Provides

This template generates projects with professional patterns, modern tooling, and comprehensive security practices:

### 🔒 Security-First Design

- **Sensitive data filtering**: Automatically masks passwords, tokens, and secrets in logs
- **Supply chain security**: SBOM generation, dependency scanning, and vulnerability auditing  
- **Security workflows**: CodeQL analysis, OpenSSF Scorecard, and automated security updates
- **Audit capabilities**: Security event tracking and compliance logging

### ⚙️ Advanced Configuration Management

- **Multiple package managers**: pip, uv, or Hatch support with optimized configurations
- **Typed configuration**: Optional Pydantic-based settings with validation and IDE support
- **Hierarchical loading**: Environment variables → Config file → Defaults
- **Environment validation**: Startup checks for required configuration

### 📊 Enhanced Logging & Observability

- **JSON-first logging**: Structured logging with request/operation ID tracking
- **Context management**: Automatic correlation IDs for distributed tracing
- **Thread-safe logging**: Safe for concurrent operations with performance optimizations
- **Flexible formats**: Switch between JSON and plain text as needed

### 🧪 Comprehensive Testing & Quality

- **Multi-environment CI**: Tests on Ubuntu and Windows with multiple Python versions
- **Security testing**: Patterns for testing sensitive data handling and configuration
- **Coverage enforcement**: 90%+ coverage requirements with quality gates
- **Type safety**: mypy integration with graduated strictness levels

### 🚀 Professional Project Types

**📚 Library Projects**: Clean package structure with modern packaging standards and comprehensive documentation

**⚡ CLI Applications**: Rich command-line interface with shell completion, man page generation, and professional help systems

### 🛡️ Supply Chain Security

- **SBOM generation**: Automatic Software Bill of Materials in CycloneDX and SPDX formats
- **Dependency auditing**: Integrated pip-audit scanning in CI workflows  
- **Vulnerability monitoring**: Automated dependency updates and security advisories
- **Attestation support**: Cryptographic verification of build artifacts

### 📖 Documentation & Developer Experience

- **Optional MkDocs**: Material theme with automatic GitHub Pages deployment
- **API documentation**: Auto-generated from docstrings with mkdocstrings
- **Configuration docs**: Auto-generated documentation for typed config schemas
- **CLI documentation**: Comprehensive usage guides and examples

> **Why these features?** These are patterns I've developed through building Python projects for business use. They solve real problems around configuration management, security compliance, and professional tooling expectations.

## Quick Start

### Prerequisites

```bash
pip install cookiecutter
```

### Generate Your Project

```bash
cookiecutter https://github.com/retr0crypticghost/python-template.git
```

You'll be prompted for project details. The template handles the complex setup automatically.

### Example Usage

```bash
$ cookiecutter https://github.com/retr0crypticghost/python-template.git

project_name [My Python Project]: Data Analysis Tool
project_slug [data-analysis-tool]:
package_name [data_analysis_tool]:
project_description [A brief description of your project]: Tool for analyzing research data
python_version [3.11]:
project_type [library]: cli-application
package_manager [pip]: uv
docs [y]: y
typed_config [n]: y
sbom [n]: y
versioning [setuptools-scm]: setuptools-scm
author_name [Your Name]: retr0crypticghost
author_email [your.email@example.com]: retr0@example.com
github_username [your-username]: retr0crypticghost
include_docker [y]: n
include_github_actions [y]: y
include_pre_commit [y]: y
license [MIT]:
```

**Result**: A fully-configured Python project with your chosen features, security practices, testing setup, and professional tooling ready for development.

## Configuration Options

The template now supports comprehensive customization:

### Project Types
- **`library`** - Python package for reusable components
- **`cli-application`** - Command-line tool with Rich interface

### Package Managers
- **`pip`** - Traditional pip-based dependency management
- **`uv`** - Ultra-fast Python package installer (recommended for speed)
- **`hatch`** - Modern Python project manager with advanced features

### Documentation
- **`docs=y`** - Scaffolds MkDocs with Material theme and GitHub Pages deployment
- **`docs=n`** - Minimal documentation setup

### Typed Configuration  
- **`typed_config=y`** - Pydantic-based settings with validation and type safety
- **`typed_config=n`** - Traditional configuration system

### Security & Compliance
- **`sbom=y`** - Software Bill of Materials generation with CycloneDX/SPDX
- **`sbom=n`** - Standard security workflows only

### Versioning Strategy
- **`setuptools-scm`** - Automatic versioning from Git tags
- **`hatch`** - Hatch-based versioning (when using Hatch package manager)
- **`manual`** - Manual version management

## Common Usage Examples

### Minimal Library Project

For a simple Python library with basic features:
```bash
cookiecutter https://github.com/retr0crypticghost/python-template.git --no-input \
  project_name="My Library" \
  project_type="library" \
  package_manager="pip" \
  docs="n" \
  typed_config="n" \
  sbom="n" \
  versioning="manual"
```

### Full-Featured CLI Application  

For a professional command-line tool with all features:
```bash
cookiecutter https://github.com/retr0crypticghost/python-template.git --no-input \
  project_name="My CLI Tool" \
  project_type="cli-application" \
  package_manager="uv" \
  docs="y" \
  typed_config="y" \
  sbom="y" \
  versioning="setuptools-scm"
```

### Enterprise Library

For a library with enterprise-grade features:
```bash
cookiecutter https://github.com/retr0crypticghost/python-template.git --no-input \
  project_name="Enterprise Library" \
  project_type="library" \
  package_manager="hatch" \
  docs="y" \
  typed_config="y" \
  sbom="y" \
  versioning="hatch"
```

### Quick Development Project

For rapid prototyping with modern tooling:
```bash
cookiecutter https://github.com/retr0crypticghost/python-template.git --no-input \
  project_name="Quick Project" \
  project_type="library" \
  package_manager="uv" \
  docs="n" \
  typed_config="y" \
  sbom="n" \
  versioning="manual"
```

## Generated Project Structure

**Clean architecture with good separation of concerns:**

```
data-analysis-tool/
├── src/
│   └── data_analysis_tool/
│       ├── __init__.py          # Package exports
│       ├── core.py              # Application logic
│       ├── config.py            # Configuration management
│       └── logger.py            # Security-aware logging
├── tests/
│   ├── __init__.py              # Test package
│   ├── test_core.py             # Functionality tests
│   ├── test_config.py           # Configuration tests
│   └── test_logger.py           # Security and logging tests
├── .env.example                 # Environment template
├── config.yaml                  # Configuration defaults
├── pyproject.toml              # Modern Python packaging with quality checks
├── README.md                   # Generated documentation
└── run_data-analysis-tool.py   # Entry point script
```

**What you get:**
- ✅ **Modern package structure** following current Python standards
- ✅ **Comprehensive test suite** with coverage requirements
- ✅ **Security-conscious logging** with automatic sensitive data filtering
- ✅ **Flexible configuration** with environment variable support
- ✅ **CI/CD ready** with GitHub Actions workflow
- ✅ **Quality tooling** with linting, type checking, and formatting

## Key Components

### Configuration System (`config.py`)

```python
from data_analysis_tool.config import get_config

config = get_config()
api_timeout = config.get('api.timeout', 30)  # Fallback to 30
database_url = config.get('database.url')    # From env or config file
```

**Configuration Hierarchy** (highest priority first):

1. Environment variables (e.g., `MYAPP_API_TIMEOUT`)
2. Configuration file (`config.yaml`)
3. Default values

### Security-Aware Logging (`logger.py`)

```python
from data_analysis_tool.logger import get_logger

logger = get_logger(__name__)
logger.info("Processing user request", extra={
    'user_id': 'user123',      # ✅ Safe to log
    'password': 'secret123'    # ❌ Automatically masked
})
```

**Security Features**:

- Automatic masking of sensitive fields (password, token, key, secret)
- Configurable allowed fields for logging
- Consistent formatting across all modules

### Environment Management

The template includes comprehensive environment variable management:

```bash
# .env.example shows required and optional variables
# All variables use PACKAGE_NAME_VARIABLE format
MYAPP_DATABASE_URL=postgresql://localhost/mydb
MYAPP_API_TIMEOUT=30
MYAPP_DEBUG=true

# Optional feature flags
MYAPP_ENABLE_CACHING=false
MYAPP_ENABLE_METRICS=true
```

**Environment Checking**:

- Validates required variables on startup
- Logs missing required variables as warnings
- Logs optional variables as info
- Supports inline documentation

### Testing Infrastructure

```python
# tests/conftest.py provides useful fixtures
def test_my_feature(mock_env_vars, temp_dir, sample_config_file):
    # Test with isolated environment
    pass
```

**Test Features**:

- Environment variable mocking
- Temporary directory creation
- Sample configuration files
- Isolated test environments

## Project Types & Examples

The template supports different project types to match your specific needs:

### 📚 **Library** (Default)
Python packages with good foundational patterns.

**Good for**: Reusable components, API clients, data processing libraries, internal tools

```bash
cookiecutter https://github.com/retr0crypticghost/python-template.git
# Choose: project_type = library
```

**What you get**:
- **Modern packaging** with `pyproject.toml` and proper dependency management
- **Security-conscious logging** with sensitive data filtering
- **Hierarchical configuration** with environment variable support
- **Comprehensive testing** with coverage requirements
- **Type safety** with mypy integration

**Usage example**:
```python
from your_library import get_logger, get_config

# Logging with automatic security filtering
logger = get_logger(__name__)
logger.info("Processing user data", extra={"user_id": "12345", "password": "secret"})
# Output: "Processing user data" {"user_id": "12345", "password": "[REDACTED]"}

# Configuration with fallbacks
config = get_config()
api_key = config.get('api.key')  # From env vars, config file, or defaults
timeout = config.get('api.timeout', 30)  # With fallback value
```

### ⚡ **CLI Application**
Command-line tools with professional features.

**Good for**: System utilities, data processors, DevOps tools, command-line interfaces

```bash
cookiecutter https://github.com/retr0crypticghost/python-template.git
# Choose: project_type = cli-application
```

**Features included**:
- **Click framework** with Rich console output and proper error handling
- **Shell completion** for bash/zsh/fish/PowerShell
- **Man page generation** for system integration
- **Professional help system** with clear command structure
- **Configuration integration** with CLI option overrides

**Usage example**:
```bash
your-tool --help                    # Rich help with examples
your-tool process-files *.csv       # Batch processing
your-tool --config prod.yaml        # Custom configuration
your-tool completion bash           # Install shell completion
man your-tool                       # System documentation
```

**Why this matters**: Creates CLI tools that feel professional and integrate well with system workflows.

### 🚀 **Future Project Types**
Additional templates planned based on actual project needs.

**🌐 API Server Template** (Planned):
- FastAPI with OpenAPI documentation
- Database integration patterns
- Authentication and basic security
- Health checks and monitoring endpoints

**🐳 Microservice Template** (Planned):
- Containerized service patterns
- Configuration for cloud deployment
- Observability and logging integration

> **Philosophy**: New types get added when I have real projects that need them, ensuring the patterns are practical and tested.

## Why Use This Template?

### **vs. Basic Templates**

**Most templates give you**: Basic project structure, minimal configuration, simple testing setup
**This template provides**: Enterprise-grade security, flexible tooling, comprehensive automation

| Feature | Basic Templates | Python Professional Template |
|---------|----------------|------------------------------|
| **Logging** | `logging.getLogger()` | JSON logging with request IDs, security filtering, context management |
| **Configuration** | Basic config.py | Typed Pydantic settings OR traditional hierarchical system |
| **Package Management** | pip only | pip, uv, or Hatch with optimized configurations |
| **CLI Tools** | argparse basics | Rich interface with completion, man pages, and context help |
| **Testing** | pytest setup | Multi-OS, multi-Python with 90%+ coverage and security testing |
| **Security** | None | SBOM generation, dependency auditing, sensitive data protection |
| **CI/CD** | Basic workflows | Multi-environment with quality gates, security scanning, SBOM |
| **Documentation** | README only | Optional MkDocs with auto-deployment and API docs |

### **Enterprise Features**

- **Supply Chain Security**: SBOM generation, dependency auditing, vulnerability scanning
- **Observability**: Request/operation ID tracking, structured JSON logging, context propagation
- **Flexibility**: Choose your package manager (pip/uv/hatch), configuration style (typed/traditional)
- **Compliance Ready**: Security workflows, audit logging, dependency management
- **Developer Experience**: Type hints, IDE support, comprehensive documentation

### **Time Savings**

- **Zero configuration**: Everything works out of the box with sensible defaults
- **No vendor lock-in**: Choose your tools (package manager, versioning, documentation)
- **Production ready**: Security patterns, logging, and monitoring built-in
- **Maintenance free**: Automated dependency updates, security scanning, and quality checks

> **Bottom Line**: Get enterprise-grade Python projects without the complexity—choose only the features you need.

## Project Types

This template supports multiple project types, each tailored for specific use cases:

### Library

- **Standard Python package structure** with modern packaging (pyproject.toml)
- **Importable modules and functions** with proper package initialization
- **Comprehensive configuration management** with environment variable support
- **Security-aware logging** with configurable levels and safe output
- **Testing framework** with pytest and coverage reporting
- **Code quality tools** (Ruff, mypy) with sensible defaults
- **Development workflow** with optional GitHub Actions, Docker, and pre-commit hooks

### CLI Application

All library features plus:
- **Click-based command-line interface** with rich help formatting
- **Rich console output** with tables, colors, and progress indicators
- **Automatic entry point** installation via `pip install`
- **Professional CLI structure** with commands, options, and error handling
- **Built-in commands**: `status`, `hello`, `info` with extensible command structure

Example CLI usage:
```bash
# After installation
my-tool --help
my-tool status
my-tool hello "World" --count 3

# Or run directly
python run_my_project.py --help
```

### Future Expansions

Planned additions include:

- **API Server type**: FastAPI-based REST services with proper routing and documentation
- **Microservice type**: Containerized services with health checks and service discovery

Each type builds upon the core library foundation while adding specialized dependencies, entry points, and starter files.

## Best Practices

### Security

- ✅ Never log sensitive data directly
- ✅ Use environment variables for secrets
- ✅ Validate configuration on startup
- ✅ Use the provided logging utilities

### Configuration

- ✅ Use the hierarchical configuration system
- ✅ Document all variables in `.env.example`
- ✅ Provide sensible defaults in `config.yaml`
- ✅ Validate required configuration early

### Testing

- ✅ Use the provided test fixtures
- ✅ Test configuration scenarios
- ✅ Mock external dependencies
- ✅ Maintain high test coverage

## Template Evolution

This template evolves based on real Python development needs and lessons learned from actual projects.

### **Recent Improvements (2024-2025)**
- **✅ Security Focus** - PII filtering, supply chain protection, vulnerability scanning
- **✅ Professional CLI** - Shell completion, man page generation, Rich interface
- **✅ Modern Tooling** - Ruff + mypy consolidation, pre-commit automation
- **✅ Quality Gates** - Multi-Python testing, coverage requirements, type checking
- **✅ Better Documentation** - MkDocs Material with automated deployment

### **Current Development**
- **Testing Patterns** - Better fixtures and testing utilities
- **Configuration Flexibility** - Schema validation, environment-specific configs
- **CLI Enhancements** - Interactive modes, better error messages

### **Future Considerations**
- API server patterns (when I build more REST APIs)
- Container deployment patterns (as I work more with Docker)
- Database integration patterns (for projects that need persistence)
- Monitoring integration (when projects need observability)

> **Approach**: Features get added when they solve real problems in actual projects, not because they're trendy or theoretically complete.

## Development Philosophy

### **Practical Over Perfect**
This template focuses on **real-world usefulness** rather than theoretical completeness:
- **Security practices** that actually matter for business applications
- **Professional tooling** that users expect from quality CLI tools
- **Testing patterns** that catch real bugs and maintain code quality
- **Configuration management** that works in different deployment environments

### **Opinionated But Flexible**
I've made specific choices about tools and patterns based on experience:
- **Ruff + mypy** for code quality (fast, comprehensive)
- **pytest** for testing (excellent ecosystem)
- **Click + Rich** for CLI tools (professional, user-friendly)
- **YAML/JSON** for configuration (widely supported, readable)

These choices reduce decision fatigue while remaining adaptable to different needs.

### **Collaborative Development**
This template benefits from **AI-human collaboration**:
- **Human experience** - Real project challenges and practical requirements
- **AI analysis** - Pattern optimization, edge case identification, code quality
- **Continuous refinement** - Regular review and improvement based on usage

The result is better than either perspective alone could produce.

## Contributing

I welcome contributions, feedback, and suggestions! This template improves through real-world usage and community input.

### 🐛 **Found a Bug?**
- Check [existing issues](https://github.com/retr0crypticghost/python-template/issues) first
- Open a new issue with details about the problem
- Include steps to reproduce and your environment

### 💡 **Have an Idea?**
- Open an issue to discuss new features or improvements
- Explain the use case and how it would help your projects
- Consider if it fits the template's philosophy of practical, needed features

### 🔧 **Want to Contribute Code?**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Test your changes with both project types (library and CLI)
4. Commit with clear messages (`git commit -m 'Add amazing feature'`)
5. Push to your branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### 📖 **Documentation Improvements**
Documentation improvements are always welcome! This includes:
- Better examples and use cases
- Clearer setup instructions
- More comprehensive troubleshooting

## License

This template is released under the [MIT License](LICENSE). Feel free to use it for any purpose, modify it to fit your needs, and share it with others.

## Acknowledgments

- Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- Developed collaboratively with AI as a coding partner
- Inspired by real-world Python development challenges and solutions

---

**Happy coding!** 🐍✨

## License

This template is released under the MIT License. Projects generated from this template can use any license you prefer.

---

**A professional template by [@retr0crypticghost](https://github.com/retr0crypticghost) - practical Python project foundations**
