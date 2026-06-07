
import click

@click.command()
@click.argument("source", type=click.Path(exists=False))
@click.argument("destination", type=click.Path(exists=False))
def compare(source, destination):
    """Compare tick data from SOURCE to DESTINATION."""
    click.echo(f"Comparing {source} → {destination}")
    # TODO: implement append logic
    if source is None:
        source = prompt_filename('Enter file source')

    if destination is None:
        destination = prompt_filename('Enter file destination')