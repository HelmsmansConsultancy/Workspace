import click
from rich.console import Console
import sys


console = Console()

@click.command()
def exit():
    """Exiting the application."""
    click.echo(f"Exiting the application...")
    sys.exit(0)


