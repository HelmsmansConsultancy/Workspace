
import click

@click.command()
@click.argument("source", type=click.Path(exists=True))
@click.argument("destination", type=click.Path())
def append(source, destination):
    """Append tick data from SOURCE into DESTINATION. (Destructive)"""
    click.echo(f"Appending {source} → {destination}")
    # TODO: implement append logic

