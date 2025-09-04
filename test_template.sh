#!/bin/bash
set -e

echo "🧪 Testing Python Template Generation..."

# Clean up any existing test projects
rm -rf test-library test-cli-app

echo "📚 Testing Library Project Generation..."
cookiecutter . --no-input \
    project_name="Test Library" \
    project_slug="test-library" \
    project_type="library"

echo "✅ Library project generated successfully"

echo "⚡ Testing CLI Application Generation..."
cookiecutter . --no-input \
    project_name="Test CLI App" \
    project_slug="test-cli-app" \
    project_type="cli-application"

echo "✅ CLI application generated successfully"

echo "🔍 Validating Generated Projects..."

# Check that key files exist
echo "  🔍 Checking library project structure..."
test -f test-library/pyproject.toml || (echo "❌ Missing pyproject.toml in library" && exit 1)
test -f test-library/src/test_library/__init__.py || (echo "❌ Missing __init__.py in library" && exit 1)
test -f test-library/tests/test_core.py || (echo "❌ Missing test file in library" && exit 1)

echo "  🔍 Checking CLI project structure..."
test -f test-cli-app/pyproject.toml || (echo "❌ Missing pyproject.toml in CLI app" && exit 1)
test -f test-cli-app/src/test_cli_app/__init__.py || (echo "❌ Missing __init__.py in CLI app" && exit 1)
test -f test-cli-app/src/test_cli_app/cli.py || (echo "❌ Missing cli.py in CLI app" && exit 1)
test -f test-cli-app/tests/test_core.py || (echo "❌ Missing test file in CLI app" && exit 1)

# Check that library doesn't have CLI files
test ! -f test-library/src/test_library/cli.py || (echo "❌ Library should not have cli.py" && exit 1)

# Check that CLI has extra files
test -f test-cli-app/run_test-cli-app.py || (echo "❌ CLI app missing run script" && exit 1)

echo "🧹 Cleaning up test projects..."
rm -rf test-library test-cli-app

echo "🎉 All validation tests passed! Template is working correctly."
