import click

@click.command()
@click.argument("filename", type=click.Path(exists=True))
def describe(filename):
    """Describe the contents of FILENAME."""
    click.echo(f"Describing: {filename}")
    # TODO: implement describe logic
    df = load_tickdata(filepath)

