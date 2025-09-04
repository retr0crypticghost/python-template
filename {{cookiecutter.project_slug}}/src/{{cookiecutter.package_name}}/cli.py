"""
Command-line interface for {{ cookiecutter.project_name }}.

This module provides the CLI entry point and command definitions.
"""

import click  # noqa: I001
from rich.console import Console
from rich.table import Table

from . import __version__, get_config, get_logger


console = Console()
logger = get_logger(__name__)


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
@click.option(
    "--config", "-c",
    type=click.Path(),
    help="Path to configuration file"
)
@click.pass_context
def cli(ctx, verbose, config):
    """
    {{ cookiecutter.project_name }} - {{ cookiecutter.project_description }}

    A professional CLI application with comprehensive logging and configuration.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Store options in context
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = config

    # Configure logging based on verbosity
    if verbose:
        logger.info("Verbose mode enabled")

    if verbose:
        logger.info("Verbose mode enabled")

    if config:
        logger.info(f"Using config file: {config}")


@cli.command()
@click.pass_context
def status(ctx):
    """Show application status and configuration."""
    config = get_config()

    # Create a status table
    table = Table(title="{{ cookiecutter.project_name }} Status")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Version", __version__)
    table.add_row("App Name", config.get('app.name', 'Unknown'))
    table.add_row("Environment", config.get('app.environment', 'development'))
    table.add_row("Log Level", config.get('logging.level', 'INFO'))
    table.add_row("Verbose Mode", str(ctx.obj.get('verbose', False)))

    console.print(table)
    logger.info("Status command executed")


@cli.command()
def completion():
    """Manage shell completion installation."""
    console.print("🔧 Shell Completion Setup")
    console.print("")
    console.print("To enable shell completion, run one of these commands:")
    console.print("")
    console.print("  [cyan]Bash:[/cyan]")
    console.print("    eval \"$({{ cookiecutter.project_slug }} --help)\"")
    console.print("    # Add this to ~/.bashrc for permanent completion")
    console.print("")
    console.print("  [cyan]Zsh:[/cyan]")
    console.print("    eval \"$({{ cookiecutter.project_slug }} --help)\"")
    console.print("    # Add this to ~/.zshrc for permanent completion")
    console.print("")
    console.print("  [cyan]Fish:[/cyan]")
    console.print("    {{ cookiecutter.project_slug }} --help | source")
    console.print("    # Add this to ~/.config/fish/config.fish for permanent completion")
    console.print("")
    console.print("Note: Restart your shell after enabling completion.")


@cli.command()
@click.argument('name', default='World')
@click.option(
    '--count', '-n',
    default=1,
    type=int,
    help='Number of greetings'
)
@click.pass_context
def hello(ctx, name, count):
    """Say hello to NAME."""
    for i in range(count):
        message = f"Hello, {name}!"
        if ctx.obj.get('verbose'):
            message += f" (greeting {i + 1}/{count})"
        console.print(message, style="bold green")

    logger.info(f"Greeted {name} {count} time(s)")


@cli.command()
@click.pass_context
def info(ctx):
    """Show detailed application information."""
    config = get_config()

    console.print("\n[bold blue]{{ cookiecutter.project_name }}[/bold blue]")
    console.print(f"Version: {__version__}")
    console.print("Description: {{ cookiecutter.project_description }}")
    console.print("Author: {{ cookiecutter.author_name }}")
    console.print("Python Version: {{ cookiecutter.python_version }}+")

    console.print("\n[bold blue]Configuration:[/bold blue]")
    config_data = config.get_all()
    for key, value in config_data.items():
        if isinstance(value, dict):
            console.print(f"  {key}:")
            for subkey, subvalue in value.items():
                console.print(f"    {subkey}: {subvalue}")
        else:
            console.print(f"  {key}: {value}")

    logger.info("Info command executed")


@cli.command(hidden=True)
@click.option(
    '--output', '-o',
    type=click.Path(),
    default='{{ cookiecutter.package_name }}.1',
    help='Output file for the man page'
)
@click.pass_context
def generate_man(ctx, output):
    """Generate man page for the CLI application."""
    try:
        import os  # noqa: PLC0415

        from click_man.core import write_man_pages  # noqa: PLC0415

        console.print(f"Generating man page: {output}")

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output) or "."
        os.makedirs(output_dir, exist_ok=True)

        # Generate the man page using write_man_pages
        write_man_pages(cli, output_dir)

        console.print(f"✅ Man page generated: {output}")
        console.print(f"Install with: sudo cp {output} /usr/local/man/man1/")
        console.print(f"View with: man {output.replace('.1', '')}")

        logger.info(f"Man page generated: {output}")

    except ImportError:
        console.print("[red]Error: click-man not installed. Install with: pip install click-man[/red]")
    except Exception as e:
        console.print(f"[red]Error generating man page: {e}[/red]")
        logger.error(f"Man page generation failed: {e}")


def main():
    """Main CLI entry point."""
    try:
        cli()
    except Exception as e:
        logger.error(f"CLI error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        raise


def generate_man_page():
    """Entry point for man page generation."""
    try:
        import os  # noqa: PLC0415
        import sys  # noqa: PLC0415

        from click_man.core import write_man_pages  # noqa: PLC0415

        if len(sys.argv) > 1:
            output_dir = sys.argv[1]
        else:
            output_dir = "."

        print(f"Generating man page in directory: {output_dir}")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate the man page
        write_man_pages(cli, output_dir)

        man_file = os.path.join(output_dir, "{{ cookiecutter.project_slug }}.1")
        print(f"✅ Man page generated: {man_file}")
        print(f"Install with: sudo cp {man_file} /usr/local/man/man1/")
        print("View with: man {{ cookiecutter.project_slug }}")

    except ImportError:
        print("Error: click-man not installed. Install with: pip install click-man")
        sys.exit(1)
    except Exception as e:
        print(f"Error generating man page: {e}")
        sys.exit(1)


# Import click_man at module level for testing compatibility
try:
    import click_man
except ImportError:
    click_man = None


if __name__ == "__main__":
    main()
