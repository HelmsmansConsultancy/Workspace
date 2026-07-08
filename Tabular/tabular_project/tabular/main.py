import click
import os
from typing import Callable 
from rich.console import Console
from tabular.service.s import S
from tabular.commands.exit import exit
from tabular.commands.metatrader5 import metatrader5
from tabular.commands.connect import connect
from tabular.commands.database import database
from tabular.commands.list import list 
from tabular.util.xmlutils import load_xml_config
from tabular.util.menuutils import interactive_menu, empty_string
from tabular.util.fileutils import pick_file
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.data.application_config import ApplicationConfig
from tabular.commands.accounts import accounts
from tabular.data.metatrader_config import MetatraderConfig

console = Console()
applicationConfig: ApplicationConfig = None
databaseService: DatabaseService = None

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
        message += " <Not connected.>"
    return message

def explain_accounts():
    if databaseService is not None:
        accounts = databaseService.countAccounts()
        if accounts > 0:
            return f"\t\t\t<{accounts} account(s)>"
        else:
            return "\t\t\t<No accounts>"
    return "\t\t\t<No database available.>"

def explain_empty():
    return empty_string
    
SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str | None]]] = [
    ['Database', database.callback.__name__, explain_DB, None], 
    ['MetaTrader 5', metatrader5.callback.__name__.replace("_", "-"), explain_MT5, None], 
    ['Accounts', accounts.callback.__name__.replace("_", "-"), explain_accounts, None],
    ['Connect', connect.callback.__name__.replace("_", "-"), explain_empty, None], 
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
    global databaseService
    global applicationConfig
    click.echo("Tabular starting...")
    applicationConfig    = ApplicationConfig()

    if bool(db_file) and db_file.endswith(".db"):
        applicationConfig.db_file = db_file
    SingletonService().put(S.APPLICATION_CONFIG, applicationConfig)
    databaseService = DatabaseService()
    SingletonService().put(S.DATABASE_SERVICE, databaseService)

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
            click.echo(f"Invoking command: {choice}")
            ctx.invoke(ctx.command.commands[choice[1]])
            result = choice[3]
            choice = None  # Reset choice to None after invoking the command
        else:
            click.echo("main.py: Back to main menu")
            return result

main.add_command(database)
main.add_command(metatrader5)
main.add_command(accounts)
main.add_command(connect)
main.add_command(list)
main.add_command(exit)

if __name__ == "__main__":
    main()