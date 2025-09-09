{%- if cookiecutter.docs == 'y' and cookiecutter.typed_config == 'y' %}
# Configuration

{{ cookiecutter.project_name }} uses a sophisticated configuration system that supports multiple sources and provides type safety when typed configuration is enabled.

## Configuration Hierarchy

Configuration is loaded in the following order (later sources override earlier ones):

1. **Default values** - Built-in sensible defaults
2. **Configuration file** - YAML or JSON file (auto-detected)  
3. **Environment variables** - OS environment variables with prefix

## Configuration Sources

### Environment Variables

All environment variables use the prefix `{{ cookiecutter.package_name|upper }}_` followed by the configuration path with double underscores (`__`) for nesting.

Examples:
```bash
# Application settings
{{ cookiecutter.package_name|upper }}_APP__NAME=my-app
{{ cookiecutter.package_name|upper }}_APP__DEBUG=true

# Logging settings  
{{ cookiecutter.package_name|upper }}_LOGGING__LEVEL=DEBUG
{{ cookiecutter.package_name|upper }}_LOGGING__FORMAT=json

# API settings
{{ cookiecutter.package_name|upper }}_API__TIMEOUT=60
{{ cookiecutter.package_name|upper }}_API__BASE_URL=https://api.example.com

# Database settings
{{ cookiecutter.package_name|upper }}_DATABASE__URL=postgresql://localhost/mydb
{{ cookiecutter.package_name|upper }}_DATABASE__POOL_SIZE=10

# Feature flags
{{ cookiecutter.package_name|upper }}_FEATURES__CACHING=false
{{ cookiecutter.package_name|upper }}_FEATURES__METRICS=true
```

### Configuration File

Create a `config.yaml` (or `config.json`) file in your project root:

```yaml
app:
  name: {{ cookiecutter.package_name }}
  debug: false
  version: "1.0.0"

logging:
  level: INFO
  format: json
  console_level: INFO
  file_level: DEBUG
  file_path: logs/{{ cookiecutter.package_name }}.log

api:
  timeout: 30
  max_retries: 3
  retry_delay: 1.0
  base_url: null

database:
  url: null
  pool_size: 5
  max_overflow: 10

security:
  secret_key: null
  encryption_key: null

features:
  caching: true
  metrics: false
```

### Environment File (.env)

Create a `.env` file for development:

```env
{{ cookiecutter.package_name|upper }}_APP__DEBUG=true
{{ cookiecutter.package_name|upper }}_LOGGING__LEVEL=DEBUG
{{ cookiecutter.package_name|upper }}_API__TIMEOUT=60
{{ cookiecutter.package_name|upper }}_DATABASE__URL=sqlite:///local.db
```

## Typed Configuration

With typed configuration enabled, you get:

- **Type safety** - All configuration values are validated
- **IDE support** - Autocompletion and type hints
- **Validation** - Automatic validation of configuration values
- **Documentation** - Built-in field descriptions

### Usage

```python
from {{ cookiecutter.package_name }}.settings import get_settings, get_app_config

# Get the full settings object
settings = get_settings()
print(settings.app.name)
print(settings.logging.level)

# Or get specific sections
app_config = get_app_config()
print(app_config.name)
print(app_config.debug)
```

### Configuration Sections

#### App Settings
```python
from {{ cookiecutter.package_name }}.settings import get_app_config

app = get_app_config()
print(f"App: {app.name} v{app.version}")
if app.debug:
    print("Debug mode enabled")
```

#### Logging Settings
```python
from {{ cookiecutter.package_name }}.settings import get_logging_config

logging = get_logging_config()
print(f"Log level: {logging.level}")
print(f"Log format: {logging.format}")
```

#### API Settings
```python
from {{ cookiecutter.package_name }}.settings import get_api_config

api = get_api_config()
print(f"API timeout: {api.timeout}s")
print(f"Max retries: {api.max_retries}")
```

#### Database Settings
```python
from {{ cookiecutter.package_name }}.settings import get_database_config

db = get_database_config()
if db.url:
    print(f"Database URL: {db.url}")
    print(f"Pool size: {db.pool_size}")
```

#### Feature Flags
```python
from {{ cookiecutter.package_name }}.settings import get_feature_config

features = get_feature_config()
if features.caching:
    print("Caching is enabled")
if features.metrics:
    print("Metrics collection is enabled")
```

## Legacy Configuration Access

For backwards compatibility, you can still use the traditional configuration API:

```python
from {{ cookiecutter.package_name }}.config import get_config

config = get_config()
app_name = config.get('app.name')
log_level = config.get('logging.level', 'INFO')
api_timeout = config.get('api.timeout', 30)
```

## Validation

Typed configuration includes built-in validation:

- **Log levels** must be valid Python logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Security keys** must be at least 32 characters long  
- **Numeric values** must be within reasonable ranges
- **Required fields** are validated at startup

Invalid configuration will raise clear error messages:

```python
# This will raise a validation error
settings = Settings(logging__level="INVALID")
# ValueError: Log level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Environment-Specific Configuration

### Development
```env
{{ cookiecutter.package_name|upper }}_APP__DEBUG=true
{{ cookiecutter.package_name|upper }}_LOGGING__LEVEL=DEBUG
{{ cookiecutter.package_name|upper }}_LOGGING__CONSOLE_LEVEL=DEBUG
```

### Production
```env
{{ cookiecutter.package_name|upper }}_APP__DEBUG=false
{{ cookiecutter.package_name|upper }}_LOGGING__LEVEL=INFO
{{ cookiecutter.package_name|upper }}_LOGGING__CONSOLE_LEVEL=WARNING
{{ cookiecutter.package_name|upper }}_DATABASE__URL=postgresql://prod-server/mydb
{{ cookiecutter.package_name|upper }}_SECURITY__SECRET_KEY=your-very-secure-32-char-secret-key
```

### Testing
```env
{{ cookiecutter.package_name|upper }}_APP__DEBUG=true
{{ cookiecutter.package_name|upper }}_LOGGING__LEVEL=WARNING
{{ cookiecutter.package_name|upper }}_DATABASE__URL=sqlite:///test.db
{{ cookiecutter.package_name|upper }}_FEATURES__CACHING=false
```
{%- endif %}