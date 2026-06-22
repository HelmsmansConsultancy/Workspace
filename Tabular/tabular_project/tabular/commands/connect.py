import click
from rich.console import Console


console = Console()

@click.command()
#@click.argument("source", default=None, required=False, type=click.Path(exists=False))
def connect():
    """Connect to a data source."""
    click.echo(f"Connecting to: ")
