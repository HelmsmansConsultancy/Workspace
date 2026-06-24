import click
from rich.console import Console

console = Console()

def accounts():
    """List all accounts."""
    click.echo("Listing all accounts...")