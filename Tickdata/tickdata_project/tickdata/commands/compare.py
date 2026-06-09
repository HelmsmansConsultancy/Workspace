
from genericpath import exists

import click
from rich.console import Console

from tickdata.util.filecompletion import prompt_filename

console = Console()

@click.command()
@click.argument("source", default=None, required=False, type=click.Path(exists=False))
@click.argument("destination", default=None, required=False, type=click.Path(exists=False))
def compare(source, destination):
    """Compare tick data from SOURCE to DESTINATION."""
    click.echo(f"Comparing {source} → {destination}")
    # TODO: implement append logic
    if source is None:
        source = prompt_filename('Enter file source')

    if destination is None:
        destination = prompt_filename('Enter file destination')
