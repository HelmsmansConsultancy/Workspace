import click
import os
from typing import Callable 
from rich.console import Console
from tabular.util.fileutils import pick_file
from tabular.util.menuutils import interactive_menu, empty_string
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.util.xmlutils import load_xml_config

console = Console()
databaseService: DatabaseService = None


def explain_empty():
    return empty_string
    

MT5_SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str]]] = [
    ['Append a MT5', 'appendMT5', explain_empty], 
    ['Delete MT5', 'delete', explain_empty], 
    ['List ', 'listMT5', explain_empty], 
    ['Return to previous menu', None, explain_empty]
]

@click.command()
def appendMT5():
    """ Select a MetaTrader 5 installation"""
    metatraderPath = pick_file(start_dir=os.getcwd())
    if bool(metatraderPath) and metatraderPath.endswith(".exe") and len(databaseService.getMetatradersByPath(metatraderPath)) == 0:
        metatraderId = databaseService.addMetatrader(metatraderPath)


@click.command()
def listMT5():
    """List all MT5 installations."""

@click.group()
@click.pass_context
def metatrader5(ctx):
    """ Load the configuration from the XML file.  """
    global databaseService
    databaseService = SingletonService().get("DatabaseService")

    mt5_installations = databaseService.listMetatraders()
    click.echo(empty_string)
    click.echo("MT5 Installations:")
    for mt5 in mt5_installations:
        click.echo(f"- {mt5}")
    else:
        click.echo("No MT5 installations found.")
    click.echo(empty_string)

    while True:
        if ctx.invoked_subcommand is None:
            choice = interactive_menu(MT5_SUB_COMMANDS)
            if choice:
                ctx.invoke(ctx.command.commands[choice])
            else:
                break

metatrader5.add_command(appendMT5)