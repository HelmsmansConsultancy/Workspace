import click
from tickdata.commands.describe import describe
from tickdata.commands.append import append

@click.group()
def tickdata():
    """Tick data management tool."""
    pass

tickdata.add_command(describe)
tickdata.add_command(append)