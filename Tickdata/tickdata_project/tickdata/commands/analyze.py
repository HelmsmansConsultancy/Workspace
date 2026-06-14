import click
from rich.console import Console

console = Console()

@click.command()
@click.argument("source", default=None, required=False, type=click.Path(exists=False))
def analyze(source):
    console.print(f"Analyzing: {source}")