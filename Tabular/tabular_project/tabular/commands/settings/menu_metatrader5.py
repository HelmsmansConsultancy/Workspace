import click
import os
from pathlib import Path
from typing import Callable
from rich.console import Console
from tabular.service.s import S
from tabular.util.util.file_utils import pick_file
from tabular.util.menu.menus_allow import empty_string, allow_allways, no_metatraders
from tabular.util.menu.menus_explain import explain_empty
from tabular.util.menu.menus_utils import interactive_menu
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.commands.settings.menu_accounts import accounts
from tabular.data.settings.account_metatrader_connection import AccountMetatraderConnection

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

@click.command()
def list_mt5():
    """ List all MetaTrader 5 installations"""
    mt5_installations = databaseService.listMetatraders()
    click.echo(empty_string)
    if len(mt5_installations) > 0:
        click.echo("MT5 Installations:")
        for mt5 in mt5_installations:
            click.echo(f"- {mt5!r}")
    else:
        click.echo("No MT5 installations found.")
    click.echo(empty_string)

@click.command()
def append_mt5():
    """ Select a MetaTrader 5 installation"""
    metatraderPath = pick_file(start_dir=os.getcwd(), file_extension=".exe")
    click.echo(f"Selected MT5 path: {metatraderPath}")
    if bool(metatraderPath) and metatraderPath.endswith(".exe") and len(databaseService.getMetatradersByPath(metatraderPath)) == 0:
        mt5_to_connect = databaseService.addMetatrader(MetatraderConfig(path=metatraderPath, name=Path(metatraderPath).parent.name))
        click.echo(f"MT5 installation added with ID: {mt5_to_connect.id} and path: {mt5_to_connect.path}")
        updated_mt5_config = metatrader5Service.connect_mt5(mt5_to_connect)
        databaseService.updateMetatrader(updated_mt5_config)
        SingletonService().put(S.CONNECTED_MT5, mt5_to_connect)
        click.echo(empty_string)
        return [accounts.callback.__name__.replace("_", "-")]

@click.command()
def connect_mt5():
    """ Connect to a MetaTrader 5 installation"""
    global databaseService
    global metatrader5Service
    click.echo(empty_string)
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
        updated_mt5_config = metatrader5Service.connect_mt5(mt5_to_connect)
        databaseService.updateMetatrader(updated_mt5_config)
        SingletonService().put(S.CONNECTED_MT5, mt5_to_connect)
        click.echo(empty_string)
    else:
        click.echo("Invalid choice. No MT5 installation connected.")
        click.echo(empty_string)
    return [accounts.callback.__name__.replace("_", "-")]

@click.command()
def disconnect_mt5():
    """ Disconnect from a MetaTrader 5 installation"""
    global metatrader5Service

    connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if connected_mt5 is not None:
        metatrader5Service.disconnect_mt5()
        SingletonService().put(S.CONNECTED_MT5, None)
        click.echo(f"Disconnected from MT5 installation: {connected_mt5.path}") 
    else:
        click.echo("No MT5 installation is currently connected.")


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


MT5_SUB_COMMANDS:  list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [ 
    [allow_allways, explain_empty,  'List all MT5', list_mt5.callback.__name__.replace("_", "-"), ], 
    [allow_allways, explain_empty,  'Append an Installation', append_mt5.callback.__name__.replace("_", "-"),],
    [no_metatraders, explain_empty, 'Connect to a MT5', connect_mt5.callback.__name__.replace("_", "-"), ],
    [no_metatraders, explain_empty,  'Disconnect from a MT5', disconnect_mt5.callback.__name__.replace("_", "-"), ],
    [no_metatraders, explain_empty, 'Delete a MT5', delete_mt5.callback.__name__.replace("_", "-"), ],
    [allow_allways, explain_empty,  'Return to previous menu', None, ]
]

@click.group()
@click.pass_context
def metatrader5(ctx):
    """Status of database."""
    global databaseService
    global metatrader5Service
    databaseService = SingletonService().get(S.DATABASE_SERVICE)
    metatrader5Service = SingletonService().get(S.METATRADER5_SERVICE)

    choice = None
    while True:
        mt5_installations: list[MetatraderConfig] = databaseService.listMetatraders()
        click.echo(empty_string)
        click.echo("MT5 Installations:")
        if bool(mt5_installations) and len(mt5_installations) > 0:
            for mt5 in mt5_installations:
                click.echo(f"- {mt5}")
                accountMetatraderConnections: AccountMetatraderConnection = databaseService.list_account_metatrader_connections_by_metatrader(mt5.id)
                for accountMetatraderConnection in accountMetatraderConnections:
                    account = databaseService.getAccount(accountMetatraderConnection.account_id)
                    click.echo(f"\t- {account}")
        else:
            click.echo("No MT5 installations found.")
        click.echo(empty_string)

        connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
        if bool(connected_mt5):
            click.echo(f"Currently connected to MT5 installation: {connected_mt5.name}")
        else:
            click.echo("Not connected to any MT5 installation.")

        if not bool(choice):
            choice = interactive_menu(MT5_SUB_COMMANDS, menuName="Settings - MetaTrader 5")
        
        if bool(choice):
            next_menu: list[str] = ctx.invoke(ctx.command.commands[choice])
            click.echo(f"Next_menu {Path(__file__).name}: {next_menu}")
            if bool(next_menu):
                    return next_menu
            else: 
                choice = None  # Reset choice to None after invoking the command
        else:
            return
                
metatrader5.add_command(append_mt5)
metatrader5.add_command(list_mt5)
metatrader5.add_command(connect_mt5)
metatrader5.add_command(disconnect_mt5)
metatrader5.add_command(delete_mt5)
