{%- if cookiecutter.docs == 'y' and cookiecutter.project_type == "cli-application" %}
# CLI Usage

{{ cookiecutter.project_name }} provides a rich command-line interface built with Click and Rich for an excellent user experience.

## Installation

After installing the package, the CLI commands become available:

```bash
# Install the package
pip install {{ cookiecutter.project_slug }}

# The main command is now available
{{ cookiecutter.package_name }} --help
```

## Available Commands

### Main Command

```bash
{{ cookiecutter.package_name }} --help
```

This shows all available commands and global options.

### Status Command

Check the application status and configuration:

```bash
{{ cookiecutter.package_name }} status
```

This command displays:
- Application name and version
- Current configuration summary
- System information
- Feature flags status

### Hello Command

Example interactive command with options:

```bash
# Simple greeting
{{ cookiecutter.package_name }} hello "World"

# Repeat the greeting
{{ cookiecutter.package_name }} hello "World" --count 3

# Use different greeting style
{{ cookiecutter.package_name }} hello "World" --style fancy
```

### Info Command

Display detailed information about the application:

```bash
{{ cookiecutter.package_name }} info
```

## Global Options

All commands support these global options:

### Configuration

```bash
# Use a specific configuration file
{{ cookiecutter.package_name }} --config config/production.yaml status

# Set log level
{{ cookiecutter.package_name }} --log-level DEBUG status

# Enable verbose output
{{ cookiecutter.package_name }} --verbose status

# Quiet mode (minimal output)
{{ cookiecutter.package_name }} --quiet status
```

### Output Formatting

```bash
# JSON output (for scripting)
{{ cookiecutter.package_name }} --output json status

# Plain text output (no colors/formatting)
{{ cookiecutter.package_name }} --output plain status

# Default rich output (colors and formatting)
{{ cookiecutter.package_name }} --output rich status
```

## Environment Variables

The CLI respects environment variables for configuration:

```bash
# Set global configuration
export {{ cookiecutter.package_name|upper }}_LOG_LEVEL=DEBUG
export {{ cookiecutter.package_name|upper }}_CONFIG_FILE=config/staging.yaml

# Command-specific settings
export {{ cookiecutter.package_name|upper }}_API_TIMEOUT=60
export {{ cookiecutter.package_name|upper }}_DATABASE_URL=postgresql://localhost/mydb

# Run command with environment config
{{ cookiecutter.package_name }} status
```

## Examples

### Basic Usage

```bash
# Check application status
{{ cookiecutter.package_name }} status

# Get detailed information
{{ cookiecutter.package_name }} info

# Simple hello world
{{ cookiecutter.package_name }} hello "{{ cookiecutter.author_name }}"
```

### Configuration Management

```bash
# Use development configuration
{{ cookiecutter.package_name }} --config config/dev.yaml status

# Use production settings with debug logging
{{ cookiecutter.package_name }} --config config/prod.yaml --log-level DEBUG status

# Override configuration with environment variables
{{ cookiecutter.package_name|upper }}_API_TIMEOUT=120 {{ cookiecutter.package_name }} status
```

### Output Formatting

```bash
# Get status as JSON (useful for scripts)
{{ cookiecutter.package_name }} --output json status

# Get quiet output (just the essentials)
{{ cookiecutter.package_name }} --quiet status

# Verbose debug information
{{ cookiecutter.package_name }} --verbose --log-level DEBUG status
```

### Batch Operations

```bash
# Process multiple items
{{ cookiecutter.package_name }} hello "Alice" "Bob" "Charlie" --count 2

# Chain commands with different configs
{{ cookiecutter.package_name }} --config dev.yaml status && \
{{ cookiecutter.package_name }} --config prod.yaml status
```

## Shell Integration

### Command Completion

Generate shell completion scripts:

```bash
# For bash
{{ cookiecutter.package_name }} completion bash > ~/.bash_completion.d/{{ cookiecutter.package_name }}

# For zsh  
{{ cookiecutter.package_name }} completion zsh > ~/.zsh/completions/_{{ cookiecutter.package_name }}

# For fish
{{ cookiecutter.package_name }} completion fish > ~/.config/fish/completions/{{ cookiecutter.package_name }}.fish

# For PowerShell
{{ cookiecutter.package_name }} completion powershell > {{ cookiecutter.package_name }}.ps1
```

### Man Page

Install the manual page:

```bash
# Generate and install man page
{{ cookiecutter.package_name }}-man

# View the man page
man {{ cookiecutter.package_name }}
```

## Exit Codes

The CLI uses standard exit codes:

- `0` - Success
- `1` - General error  
- `2` - Command line usage error
- `3` - Configuration error
- `4` - Network/API error
- `5` - File system error

Example usage in scripts:

```bash
#!/bin/bash

if {{ cookiecutter.package_name }} status --quiet; then
    echo "Application is healthy"
else
    echo "Application check failed with exit code $?"
    exit 1
fi
```

## Error Handling

The CLI provides helpful error messages:

```bash
# Invalid command
{{ cookiecutter.package_name }} invalid-command
# Error: No such command 'invalid-command'.

# Missing required argument
{{ cookiecutter.package_name }} hello
# Error: Missing argument 'name'.

# Configuration error
{{ cookiecutter.package_name }} --config missing.yaml status  
# Error: Configuration file 'missing.yaml' not found.
```

## Debugging

### Verbose Mode

```bash
# Enable verbose output
{{ cookiecutter.package_name }} --verbose status

# Debug logging
{{ cookiecutter.package_name }} --log-level DEBUG status

# Both verbose and debug
{{ cookiecutter.package_name }} --verbose --log-level DEBUG status
```

### Configuration Debugging

```bash
# Show effective configuration
{{ cookiecutter.package_name }} --verbose status

# Test configuration loading
{{ cookiecutter.package_name }} --config test.yaml --verbose status

# Show environment variable usage
{{ cookiecutter.package_name|upper }}_DEBUG=true {{ cookiecutter.package_name }} --verbose status
```

## Integration Examples

### Shell Scripts

```bash
#!/bin/bash
set -e

# Configuration
CONFIG_FILE="${CONFIG_FILE:-config/default.yaml}"
LOG_LEVEL="${LOG_LEVEL:-INFO}"

# Check application health
if ! {{ cookiecutter.package_name }} --config "$CONFIG_FILE" --log-level "$LOG_LEVEL" status --quiet; then
    echo "❌ Health check failed" >&2
    exit 1
fi

echo "✅ Application is healthy"
```

### Docker Integration

```dockerfile
FROM python:3.11-slim

# Install application
COPY . /app
WORKDIR /app
RUN pip install -e .

# Set up configuration
ENV {{ cookiecutter.package_name|upper }}_CONFIG_FILE=/app/config/docker.yaml
ENV {{ cookiecutter.package_name|upper }}_LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD {{ cookiecutter.package_name }} status --quiet || exit 1

# Default command
CMD ["{{ cookiecutter.package_name }}", "status"]
```

### CI/CD Integration

```yaml
# GitHub Actions example
steps:
  - name: Install application
    run: pip install {{ cookiecutter.project_slug }}
    
  - name: Validate configuration
    run: {{ cookiecutter.package_name }} --config config/ci.yaml status
    
  - name: Run health check
    run: {{ cookiecutter.package_name }} status --output json > health.json
```
{%- endif %}