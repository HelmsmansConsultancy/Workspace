import click

from tickdata.data.csvfile import CsvFile
from tickdata.util.csvutils import load_tickdata

@click.command()
@click.argument("filename", type=click.Path(exists=True))
def describe(filename):
    """Describe the contents of FILENAME."""
    click.echo(f"Describing: {filename}")
    # TODO: implement describe logic
    csvFile = load_tickdata(filename)

