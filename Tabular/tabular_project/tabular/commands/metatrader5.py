import click
import os
import MetaTrader5 as meta_trader_5
from MetaTrader5 import TerminalInfo
from typing import Callable, Optional 
from rich.console import Console
from tabular.util.fileutils import pick_file
from tabular.util.menuutils import interactive_menu, empty_string
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.data.metatrader_config import MetatraderConfig
from tabular.util.xmlutils import load_xml_config

console = Console()
databaseService: DatabaseService = None

def explain_empty():
    return empty_string
    
@click.command()
def delete_mt5():
    """ Delete a MetaTrader 5 installation"""
    mt5_installations = databaseService.listMetatraders()
    if len(mt5_installations) == 0:
        click.echo("No MT5 installations found.")
        return

    click.echo("Select a MT5 installation to delete:")
    for index, mt5 in enumerate(mt5_installations, start=1):
        click.echo(f"{index}. {mt5}")

    choice = click.prompt("Enter the number of the MT5 installation to delete", type=int)
    if 1 <= choice <= len(mt5_installations):
        mt5_to_delete = mt5_installations[choice - 1]
        databaseService.deleteMetatrader(mt5_to_delete.id)
        click.echo(f"Deleted MT5 installation: {mt5_to_delete}")
    else:
        click.echo("Invalid choice. No MT5 installation deleted.")


@click.command()
def append_mt5():
    """ Select a MetaTrader 5 installation"""
    metatraderPath = pick_file(start_dir=os.getcwd(), file_extension=".exe")
    click.echo(f"Selected MT5 path: {metatraderPath}")
    if bool(metatraderPath) and metatraderPath.endswith(".exe") and len(databaseService.getMetatradersByPath(metatraderPath)) == 0:
        metatraderId = databaseService.addMetatrader(MetatraderConfig(path=metatraderPath))
        click.echo(f"MT5 installation added with ID: {metatraderId} and path: {metatraderPath}")

@click.command()
def list_mt5():
    """ List all MetaTrader 5 installations"""
    mt5_installations = databaseService.listMetatraders()
    click.echo(empty_string)
    if len(mt5_installations) > 0:
        click.echo("MT5 Installations:")
        for mt5 in mt5_installations:
            click.echo(f"- {mt5}")
    else:
        click.echo("No MT5 installations found.")
    click.echo(empty_string)

@click.command()
def connect_mt5():
    """ Connect to a MetaTrader 5 installation"""
    mt5_installations: list[MetatraderConfig] = databaseService.listMetatraders()
    if len(mt5_installations) == 0:
        click.echo("No MT5 installations found.")
        return

    click.echo("Select a MT5 installation to connect to:")
    for index, mt5 in enumerate(mt5_installations, start=1):
        click.echo(f"{index}. {mt5}")

    choice = click.prompt("Enter the number of the MT5 installation to connect to", type=int)
    if 1 <= choice <= len(mt5_installations):
        mt5_to_connect: MetatraderConfig = mt5_installations[choice - 1]
        # Perform connection logic here
        meta_trader_5.initialize(path=mt5_to_connect.path)

        term_info: TerminalInfo | None = meta_trader_5.terminal_info()
        if term_info is None or not term_info.connected:
            click.echo(f"Terminal not connected to broker: {meta_trader_5.last_error()}")
        else:
            click.echo(f"Connected to MT5 installation: {term_info}")
            if term_info.connected:
                SingletonService().put("MT5TerminalInfo", term_info)
                if mt5_to_connect.terminal_version is None or mt5_to_connect.build is None or mt5_to_connect.release_date is None:
                    version_info: Optional[tuple[int, int, str]] = meta_trader_5.version()
                    mt5_to_connect.terminal_version = f"{version_info[0]}.{version_info[1]} {version_info[2]}"
                    mt5_to_connect.build = version_info[1]
                    mt5_to_connect.release_date = version_info[2]
                    databaseService.updateMetatrader(mt5_to_connect)
    else:
        click.echo("Invalid choice. No MT5 installation connected.")

MT5_SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str]]] = [
    ['Append a MT5', append_mt5.callback.__name__.replace("_", "-"), explain_empty], 
    ['List all MT5', list_mt5.callback.__name__.replace("_", "-"), explain_empty], 
    ['Connect to a MT5', connect_mt5.callback.__name__.replace("_", "-"), explain_empty],
    ['Delete a MT5', delete_mt5.callback.__name__.replace("_", "-"), explain_empty],
    ['Return to previous menu', None, explain_empty]
]

@click.group()
@click.pass_context
def metatrader5(ctx):
    """ Load the configuration from the XML file.  """
    global databaseService
    databaseService = SingletonService().get("DatabaseService")

    mt5_installations = databaseService.listMetatraders()
    click.echo(empty_string)
    click.echo("MT5 Installations:")
    if bool(mt5_installations) and len(mt5_installations) > 0:
        for mt5 in mt5_installations:
            click.echo(f"- {mt5}")
    else:
        click.echo("No MT5 installations found.")
    click.echo(empty_string)
    #    click.echo(list(ctx.command.commands))

    while True:
        if ctx.invoked_subcommand is None:
            choice = interactive_menu(MT5_SUB_COMMANDS)
            if choice:
                ctx.invoke(ctx.command.commands[choice])
            else:
                break

metatrader5.add_command(append_mt5)
metatrader5.add_command(list_mt5)
metatrader5.add_command(connect_mt5)
metatrader5.add_command(delete_mt5)