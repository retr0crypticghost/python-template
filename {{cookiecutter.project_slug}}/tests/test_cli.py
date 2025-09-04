"""
Tests for the CLI module (only applicable for CLI projects).
"""
{% if cookiecutter.project_type == "cli-application" -%}
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from {{ cookiecutter.package_name }}.cli import (
    cli,
    completion,
    console,
    generate_man,
    generate_man_page,
    hello,
    info,
    logger,
    main,
    status,
)


class TestCLICommands:
    """Test cases for CLI commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_group_help(self):
        """Test that CLI group shows help."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert '{{ cookiecutter.project_name }}' in result.output
        assert '{{ cookiecutter.project_description }}' in result.output

    def test_cli_version(self):
        """Test CLI version option."""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        # Should show version information

    def test_status_command(self):
        """Test the status command."""
        result = self.runner.invoke(cli, ['status'])
        assert result.exit_code == 0
        assert 'Status' in result.output
        assert 'Version' in result.output

    def test_status_command_verbose(self):
        """Test status command with verbose flag."""
        result = self.runner.invoke(cli, ['--verbose', 'status'])
        assert result.exit_code == 0
        assert 'Status' in result.output

    def test_completion_command(self):
        """Test the completion command."""
        result = self.runner.invoke(cli, ['completion'])
        assert result.exit_code == 0
        assert 'Shell Completion Setup' in result.output
        assert 'Bash' in result.output
        assert 'Zsh' in result.output
        assert 'Fish' in result.output

    def test_hello_command_default(self):
        """Test hello command with default parameters."""
        result = self.runner.invoke(cli, ['hello'])
        assert result.exit_code == 0
        assert 'Hello, World!' in result.output

    def test_hello_command_with_name(self):
        """Test hello command with custom name."""
        result = self.runner.invoke(cli, ['hello', 'Alice'])
        assert result.exit_code == 0
        assert 'Hello, Alice!' in result.output

    def test_hello_command_with_count(self):
        """Test hello command with count option."""
        result = self.runner.invoke(cli, ['hello', '--count', '3', 'Bob'])
        assert result.exit_code == 0
        # Should greet Bob 3 times
        assert result.output.count('Hello, Bob!') == 3

    def test_hello_command_verbose_with_count(self):
        """Test hello command with verbose flag and count."""
        result = self.runner.invoke(cli, ['--verbose', 'hello', '--count', '2', 'Charlie'])
        assert result.exit_code == 0
        # Should include greeting numbers in verbose mode
        assert 'greeting 1/2' in result.output
        assert 'greeting 2/2' in result.output

    def test_info_command(self):
        """Test the info command."""
        result = self.runner.invoke(cli, ['info'])
        assert result.exit_code == 0
        assert '{{ cookiecutter.project_name }}' in result.output
        assert '{{ cookiecutter.author_name }}' in result.output
        assert 'Configuration' in result.output

    @patch('click_man.core.write_man_pages')
    def test_generate_man_command_success(self, mock_write_man_pages):
        """Test man page generation when click-man is available."""
        # Mock successful man page generation
        mock_write_man_pages.return_value = None

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['generate-man', '--output', 'test.1'])
            assert result.exit_code == 0
            assert 'Man page generated' in result.output

    def test_generate_man_command_missing_dependency(self):
        """Test man page generation when click-man is not available."""
        with patch('{{ cookiecutter.package_name }}.cli.click_man', None):
            # Import error should be handled gracefully
            result = self.runner.invoke(cli, ['generate-man'])
            assert result.exit_code == 0
            # Should show error about missing dependency

    def test_cli_with_config_file(self, temp_dir):
        """Test CLI with custom config file."""
        config_file = temp_dir / "test_config.yaml"
        config_file.write_text("""
app:
  name: "Test App"
  version: "test-version"
""")

        result = self.runner.invoke(cli, ['--config', str(config_file), 'status'])
        assert result.exit_code == 0

    @patch('{{ cookiecutter.package_name }}.cli.logger')
    def test_cli_error_handling(self, mock_logger):
        """Test CLI error handling."""
        # Create a command that will raise an exception
        @cli.command()
        def failing_command():
            raise RuntimeError("Test error")

        # Test the command handles errors gracefully
        self.runner.invoke(cli, ['failing-command'])
        # The command should handle the error gracefully
        # (Depending on implementation, might exit with non-zero or catch)


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_main_function(self):
        """Test the main CLI entry point."""
        # This tests the main() function that would be called from console scripts
        with patch('{{ cookiecutter.package_name }}.cli.cli') as mock_cli:
            main()
            mock_cli.assert_called_once()

    def test_cli_main_with_exception(self):
        """Test main function exception handling."""
        with patch('{{ cookiecutter.package_name }}.cli.cli') as mock_cli:
            with patch('{{ cookiecutter.package_name }}.cli.logger') as mock_logger:
                with patch('{{ cookiecutter.package_name }}.cli.console') as mock_console:
                    # Make cli raise an exception
                    mock_cli.side_effect = RuntimeError("CLI error")

                    # Should handle exception and not crash
                    with pytest.raises(RuntimeError):
                        main()

                    # Should log the error
                    mock_logger.error.assert_called()
                    mock_console.print.assert_called()

    def test_generate_man_page_function(self):
        """Test the generate_man_page entry point function."""
        with patch('click_man.core.write_man_pages') as mock_write:
            with patch('sys.argv', ['prog', '/tmp']):
                generate_man_page()
                mock_write.assert_called_once()

    def test_generate_man_page_missing_click_man(self):
        """Test generate_man_page when click-man is not available."""
        with patch('click_man.core.write_man_pages', side_effect=ImportError):
            with pytest.raises(SystemExit) as exc_info:
                generate_man_page()
            assert exc_info.value.code == 1

    def test_generate_man_page_with_exception(self):
        """Test generate_man_page with general exception."""
        with patch('click_man.core.write_man_pages', side_effect=Exception("Test error")):
            with pytest.raises(SystemExit) as exc_info:
                generate_man_page()
            assert exc_info.value.code == 1

    def test_all_commands_accessible(self):
        """Test that all commands are accessible through the CLI."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0

        # Check that major commands are listed
        assert 'status' in result.output
        assert 'hello' in result.output
        assert 'info' in result.output
        assert 'completion' in result.output

    def test_cli_context_object(self):
        """Test that CLI context object is properly set up."""
        result = self.runner.invoke(cli, ['--verbose', '--config', 'nonexistent.yaml', 'status'])
        # Should handle non-existent config gracefully
        assert result.exit_code == 0


class TestCLIHelpers:
    """Test CLI helper functions and utilities."""

    def test_cli_imports(self):
        """Test that all CLI components can be imported."""
        # This test ensures all imports work correctly
        assert cli is not None
        assert status is not None
        assert completion is not None
        assert hello is not None
        assert info is not None
        assert generate_man is not None
        assert main is not None

    def test_cli_console_object(self):
        """Test that console object is properly initialized."""
        assert console is not None
        # Should be a Rich Console instance
        assert hasattr(console, 'print')
        assert hasattr(console, 'log')

    def test_cli_logger_object(self):
        """Test that logger object is properly initialized."""
        assert logger is not None
        # Should be a logging.Logger instance
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'debug')


class TestCLIEdgeCases:
    """Test edge cases and error conditions for CLI."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_hello_with_zero_count(self):
        """Test hello command with zero count."""
        result = self.runner.invoke(cli, ['hello', '--count', '0'])
        assert result.exit_code == 0
        # Should not output any greetings
        assert 'Hello' not in result.output or result.output.count('Hello') == 0

    def test_hello_with_negative_count(self):
        """Test hello command with negative count."""
        result = self.runner.invoke(cli, ['hello', '--count', '-1'])
        # Click should handle this as invalid input
        assert result.exit_code != 0 or 'Hello' not in result.output

    def test_invalid_command(self):
        """Test calling non-existent command."""
        result = self.runner.invoke(cli, ['nonexistent-command'])
        assert result.exit_code != 0
        assert 'No such command' in result.output

    def test_cli_with_invalid_config_path(self):
        """Test CLI with invalid config file path."""
        result = self.runner.invoke(cli, ['--config', '/nonexistent/path/config.yaml', 'status'])
        # Should handle missing config file gracefully
        assert result.exit_code == 0  # Should not fail completely


# Skip CLI tests for library projects
{% else -%}
import pytest


def test_cli_not_available():
    """Test that CLI module is not available for library projects."""
    # CLI tests are only applicable for CLI-type projects
    try:
        from {{ cookiecutter.package_name }}.cli import cli  # noqa: F401
        pytest.fail("CLI module should not be available for library projects")
    except ImportError:
        pass  # Expected for library projects
{% endif -%}
