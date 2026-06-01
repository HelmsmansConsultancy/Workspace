"""
ohlc_tools.cli
==============

Root `ohlc` command group.  All sub-commands are registered here.
"""

import click

from ohlc_tools import __version__
from ohlc_tools.commands.describe import cli as describe_cmd
from ohlc_tools.commands.convert import cli as convert_cmd
from ohlc_tools.commands.resample import cli as resample_cmd


@click.group()
@click.version_option(version=__version__, prog_name="ohlc-tools")
def main() -> None:
    """OHLC Tools — analyse and manipulate OHLC CSV data from the command line."""


main.add_command(describe_cmd, name="describe")
main.add_command(convert_cmd,  name="convert")
main.add_command(resample_cmd, name="resample")


if __name__ == "__main__":
    main()
