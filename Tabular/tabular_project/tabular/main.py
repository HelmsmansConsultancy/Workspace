import click
import os
import sys
from typing import Callable 
from rich.console import Console
from tabular.service.s import S
from tabular.commands.metatrader5 import metatrader5
from tabular.commands.database import database
from tabular.commands.symbols import symbols
from tabular.commands.pending_orders import pending_orders
from tabular.commands.list import list 
from tabular.util.menuutils import interactive_menu, empty_string
from tabular.util.fileutils import pick_file
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.data.application_config import ApplicationConfig
from tabular.commands.accounts import accounts
from tabular.data.metatrader_config import MetatraderConfig

console = Console()
applicationConfig: ApplicationConfig = None
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

def explain_DB():
    if databaseService is not None:
        return f"\t\t\t<{databaseService.db_file}>"
    return "\t\t\t<No database available.>"

def explain_MT5():
    message = ""
    if databaseService is not None:
        mt5_installations = databaseService.countMetatraders()
        if mt5_installations > 0:
            message = f"\t\t<{mt5_installations} MT5 installation(s)>"
        else:
            message = "\t\t<No MT5 installations found.>"
    else:
        message = "\t\t<No database available.>"

    connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if bool(connected_mt5):
        message += f" <Connected to: {connected_mt5.name}>"
    else:
        message += " <Not connected>"
    return message

def explain_accounts():
    message = ""
    if databaseService is not None:
        accounts = databaseService.countAccounts()
        if accounts > 0:
            message = f"\t\t\t<{accounts} account(s)>"
        else:
            message = "\t\t\t<No accounts>"
    else:
        message = "\t\t\t<No database available.>"

    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    if bool(connected_account):
        message += f" <Connected with: {connected_account.name}>"
    else:
        message += " <Not connected>"
    return message

def explain_empty():
    return empty_string


@click.command()
def exit():
    """Exiting the application."""
    global metatrader5Service

    metatrader5Service.disconnect_mt5()
    click.echo(f"Exiting the application...")
    sys.exit(0)



    
SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str | None]]] = [
    ['Database', database.callback.__name__, explain_DB, None], 
    ['MetaTrader 5', metatrader5.callback.__name__.replace("_", "-"), explain_MT5, None], 
    ['Accounts', accounts.callback.__name__.replace("_", "-"), explain_accounts, None],
    ['Symbols', symbols.callback.__name__.replace("_", "-"), explain_empty, None], 
    ['Pending Orders', pending_orders.callback.__name__.replace("_", "-"), explain_empty, None], 
    ['List', list.callback.__name__.replace("_", "-"), explain_empty, None], 
    ['Exit nicely', exit.callback.__name__.replace("_", "-"), explain_empty, None]
]

@click.group(invoke_without_command=True)
@click.option(
    "--db_file",
    "db_file",
    type=click.Path(),
    default=None,  # resolved lazily below so it reflects sys.argv[0] correctly
    help="Path to the SQLite database file. Defaults to <script_name>.db",
)
@click.pass_context
def main(ctx: click.Context, db_file: str):
    """Tabular MT5 data management tool."""
    click.echo("Tabular starting...")
    global databaseService
    global metatrader5Service
    global applicationConfig

    applicationConfig    = ApplicationConfig()
    if bool(db_file) and db_file.endswith(".db"):
        applicationConfig.db_file = db_file
    SingletonService().put(S.APPLICATION_CONFIG, applicationConfig)

    databaseService = DatabaseService()
    SingletonService().put(S.DATABASE_SERVICE, databaseService)

    metatrader5Service = Metatrader5Service()
    SingletonService().put(S.METATRADER5_SERVICE, metatrader5Service)

    start_dir=os.getcwd()
    SingletonService().put(S.START_DIR, start_dir)
    accounts = databaseService.accounts()
    SingletonService().put(S.ACCOUNTS, accounts)

    choice = None
    while True:
        click.echo(empty_string)
        click.echo(f"Managing {len(accounts)} account(s)")
        if choice is None:
            choice = interactive_menu(SUB_COMMANDS)
        else:
            break
        
        result = None
        if bool(choice) and bool(choice[1]):
            ctx.invoke(ctx.command.commands[choice[1]])
            result = choice[3]
            choice = None  # Reset choice to None after invoking the command
        else:
            click.echo("main.py: Back to main menu")
            return result

main.add_command(database)
main.add_command(metatrader5)
main.add_command(accounts)
main.add_command(symbols)
main.add_command(pending_orders)
main.add_command(list)
main.add_command(exit)

if __name__ == "__main__":
    main()