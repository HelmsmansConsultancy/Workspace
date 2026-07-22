import click
# from pathlib import Path
from rich.console import Console
from typing import Callable
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.service.s import S
from tabular.util.menu.menus_allow import empty_string, allow_allways
from tabular.util.menu.menus_explain import explain_accounts, explain_DB, explain_empty, explain_MT5
from tabular.util.menu.menus_utils import interactive_menu
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.commands.settings.menu_metatrader5 import metatrader5
from tabular.commands.settings.menu_database import database
from tabular.commands.settings.menu_accounts import accounts
from tabular.util.menu.menus_explain import explain_accounts, explain_empty, explain_MT5

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None


SETTINGS_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [allow_allways, explain_DB,'Database', database.callback.__name__, ], 
    [allow_allways, explain_MT5, 'MetaTrader 5', metatrader5.callback.__name__.replace("_", "-"), ], 
    [allow_allways, explain_accounts, 'Accounts', accounts.callback.__name__.replace("_", "-"), ],
    [allow_allways, explain_empty, 'Return to previous menu', None, ]
]

@click.group()
@click.pass_context
def settings(ctx: click.Context):
    """Tabular MT5 data management tool."""
    click.echo("Tabular starting...")
    global databaseService
    global metatrader5Service
    global ApplicationConfig

    databaseService = SingletonService().get(S.DATABASE_SERVICE)
    metatrader5Service = SingletonService().get(S.METATRADER5_SERVICE)

    accounts = databaseService.listAccountConfigs()

    choice = None
    while True:
        click.echo(empty_string)
        
        message: None
        if databaseService is not None:
            message = f"<{databaseService.db_file}>"
        else:
            message = "<No database available>"
        
        if databaseService is not None:
            mt5_installations = databaseService.countMetatraderConfigs()
            if mt5_installations > 0:
                message += f" <{mt5_installations} MT5(s)>"
            else:
                message += " <No MT5 found.>"
        else:
            message += " <No database available>"

        connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
        if bool(connected_mt5):
            message += f" <Conned to: {connected_mt5.name}>"
        else:
            message += " <Not connected>"
        

        if databaseService is not None:
            accounts = databaseService.countAccounts()
            if accounts > 0:
                message += f" <{accounts} account(s)>"
            else:
                message += " <No accounts>"
        else:
            message += "<No DB available>"

        connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
        if bool(connected_account):
            message += f" <Conned with: {connected_account.name}>"
        else:
            message += " <Not connected>"
        
        click.echo(message)

        if not bool(choice):
            choice = interactive_menu(SETTINGS_SUB_COMMANDS, menuName="Settings - Overview")
        
        if bool(choice):
            next_menu: list[str] = ctx.invoke(ctx.command.commands[choice])
            # click.echo(f"Next_menu {Path(__file__).name}: {next_menu}")
            if bool(next_menu):
                if len(next_menu) > 1:
                    return next_menu[1:]
                else:
                    choice = next_menu[0]
            else:
                choice = None  # Reset choice to None after invoking the command
        else:
            return


settings.add_command(database)
settings.add_command(metatrader5)
settings.add_command(accounts)