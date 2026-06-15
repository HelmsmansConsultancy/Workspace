from email.policy import default
import click
from rich.console import Console
from rich.table import Table
from rich import box


@click.command()
@click.argument("source", default=None, required=False, type=click.Path(exists=False))
def analyze(source):
    """Analyze the contents of FILENAME."""