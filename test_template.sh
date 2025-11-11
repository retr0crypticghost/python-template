#!/bin/bash
set -e

echo "🧪 Testing Python Template Generation with Enhanced Options..."

# Test all combinations of key features
test_combinations=(
    # Format: "name:project_type:package_manager:docs:typed_config:sbom:versioning"
    "library-pip-basic:library:pip:n:n:n:manual"
    "library-pip-full:library:pip:y:y:y:setuptools-scm"
    "cli-uv-basic:cli-application:uv:n:n:n:manual"
    "cli-hatch-full:cli-application:hatch:y:y:y:hatch"
    "library-uv-typed:library:uv:y:y:n:manual"
    "cli-pip-sbom:cli-application:pip:n:n:y:setuptools-scm"
)

echo "🔧 Testing ${#test_combinations[@]} different combinations..."

for combo in "${test_combinations[@]}"; do
    IFS=':' read -r name project_type package_manager docs typed_config sbom versioning <<< "$combo"
    
    echo "📦 Testing: $name"
    echo "  - Project Type: $project_type"
    echo "  - Package Manager: $package_manager"  
    echo "  - Docs: $docs"
    echo "  - Typed Config: $typed_config"
    echo "  - SBOM: $sbom"
    echo "  - Versioning: $versioning"
    
    # Clean up any existing test project
    rm -rf "test-$name"
    
    # Generate project with specific options
    cookiecutter . --no-input \
        project_name="Test $name" \
        project_slug="test-$name" \
        project_type="$project_type" \
        package_manager="$package_manager" \
        docs="$docs" \
        typed_config="$typed_config" \
        sbom="$sbom" \
        versioning="$versioning" \
        include_docker="n" \
        include_github_actions="y" \
        include_pre_commit="y" \
        license="MIT"
    
    echo "✅ Generated: test-$name"
done

echo "🔍 Validating Generated Projects..."

# Validate each generated project
for combo in "${test_combinations[@]}"; do
    IFS=':' read -r name project_type package_manager docs typed_config sbom versioning <<< "$combo"
    project_dir="test-$name"
    # The package name is derived from the full project slug (test-$name)
    full_project_slug="test-$name"
    package_name=$(echo "$full_project_slug" | tr '-' '_')
    
    echo "  🔍 Validating: $project_dir (package: $package_name)"
    
    # Check basic structure
    test -f "$project_dir/pyproject.toml" || (echo "❌ Missing pyproject.toml in $project_dir" && exit 1)
    test -f "$project_dir/src/$package_name/__init__.py" || (echo "❌ Missing __init__.py in $project_dir" && exit 1)
    test -f "$project_dir/src/$package_name/config.py" || (echo "❌ Missing config.py in $project_dir" && exit 1)
    test -f "$project_dir/src/$package_name/logger.py" || (echo "❌ Missing logger.py in $project_dir" && exit 1)
    test -d "$project_dir/tests" || (echo "❌ Missing tests directory in $project_dir" && exit 1)
    
    # Check project type specific files
    if [ "$project_type" = "cli-application" ]; then
        test -f "$project_dir/src/$package_name/cli.py" || (echo "❌ CLI project missing cli.py" && exit 1)
        test -f "$project_dir/run_test-$name.py" || (echo "❌ CLI project missing run script" && exit 1)
        test -f "$project_dir/tests/test_cli.py" || (echo "❌ CLI project missing CLI tests" && exit 1)
    else
        test ! -f "$project_dir/src/$package_name/cli.py" || (echo "❌ Library should not have cli.py" && exit 1)
        test ! -f "$project_dir/run_test-$name.py" || (echo "❌ Library should not have run script" && exit 1)
        test ! -f "$project_dir/tests/test_cli.py" || (echo "❌ Library should not have CLI tests" && exit 1)
    fi
    
    # Check docs option
    if [ "$docs" = "y" ]; then
        test -f "$project_dir/mkdocs.yml" || (echo "❌ Docs enabled but mkdocs.yml missing" && exit 1)
        test -d "$project_dir/docs" || (echo "❌ Docs enabled but docs directory missing" && exit 1)
        test -f "$project_dir/.github/workflows/docs.yml" || (echo "❌ Docs enabled but docs workflow missing" && exit 1)
    else
        test ! -f "$project_dir/mkdocs.yml" || (echo "❌ Docs disabled but mkdocs.yml exists" && exit 1)
        test ! -d "$project_dir/docs" || (echo "❌ Docs disabled but docs directory exists" && exit 1)
        test ! -f "$project_dir/.github/workflows/docs.yml" || (echo "❌ Docs disabled but docs workflow exists" && exit 1)
    fi
    
    # Check typed_config option
    if [ "$typed_config" = "y" ]; then
        test -f "$project_dir/src/$package_name/settings.py" || (echo "❌ Typed config enabled but settings.py missing" && exit 1)
        test -f "$project_dir/tests/test_settings.py" || (echo "❌ Typed config enabled but settings tests missing" && exit 1)
    else
        test ! -f "$project_dir/src/$package_name/settings.py" || (echo "❌ Typed config disabled but settings.py exists" && exit 1)
    fi
    
    # Check SBOM option
    if [ "$sbom" = "y" ]; then
        test -f "$project_dir/.github/workflows/sbom.yml" || (echo "❌ SBOM enabled but workflow missing" && exit 1)
    else
        test ! -f "$project_dir/.github/workflows/sbom.yml" || (echo "❌ SBOM disabled but workflow exists" && exit 1)
    fi
    
    # Check versioning in pyproject.toml
    if [ "$versioning" = "setuptools-scm" ]; then
        grep -q "setuptools_scm" "$project_dir/pyproject.toml" || (echo "❌ setuptools-scm versioning but no setuptools_scm config" && exit 1)
    elif [ "$versioning" = "hatch" ] && [ "$package_manager" = "hatch" ]; then
        grep -q "hatch.version" "$project_dir/pyproject.toml" || (echo "❌ Hatch versioning but no hatch.version config" && exit 1)
    fi
    
    echo "    ✅ Structure validation passed"
done

echo "🧹 Cleaning up test projects..."
for combo in "${test_combinations[@]}"; do
    IFS=':' read -r name project_type package_manager docs typed_config sbom versioning <<< "$combo"
    rm -rf "test-$name"
done

echo "🎉 All validation tests passed! Enhanced template is working correctly."

# Test basic functionality with a simple generation
echo "🚀 Testing basic functionality with library generation..."
rm -rf test-functionality
cookiecutter . --no-input \
    project_name="Test Functionality" \
    project_slug="test-functionality" \
    project_type="library" \
    package_manager="pip" \
    docs="n" \
    typed_config="n" \
    sbom="n" \
    versioning="manual"

echo "✅ Basic functionality test passed!"
rm -rf test-functionality

echo "🎉 All enhanced template tests completed successfully!"
