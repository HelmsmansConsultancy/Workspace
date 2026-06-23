import click
import sys
from rich.console import Console

from ..commands.connect import disconnect


console = Console()

@click.command()
def exit():
    """Exiting the application."""
    disconnect()
    click.echo(f"Exiting the application...")
    sys.exit(0)


