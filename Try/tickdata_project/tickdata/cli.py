import click


@click.group()
def tickdata():
    """Tick data management tool."""
    pass


@tickdata.command()
@click.argument("filename", type=click.Path(exists=True))
def describe(filename):
    """Describe the contents of FILENAME.

    FILENAME is the tick data file to inspect.
    """
    click.echo(f"Describing: {filename}")
    # TODO: implement describe logic


@tickdata.command()
@click.argument("source", type=click.Path(exists=True))
@click.argument("destination", type=click.Path())
def append(source, destination):
    """Append tick data from SOURCE into DESTINATION.

    SOURCE is the file whose data will be appended.
    DESTINATION is the file to append into.
    """
    click.echo(f"Appending {source} → {destination}")
    # TODO: implement append logic


if __name__ == "__main__":
    tickdata()
