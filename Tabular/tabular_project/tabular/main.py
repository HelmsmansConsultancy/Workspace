import click
import os
from typing import Callable 
from rich.console import Console
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

console = Console()
applicationConfig: ApplicationConfig = None
databaseService: DatabaseService = None

def explain_DB():
    if databaseService is not None:
        return f"<{databaseService.db_file}>"
    return "<No database available.>"

def explain_MT5():
    if databaseService is not None:
        mt5_installations = databaseService.countMetatraders()
        if mt5_installations > 0:
            return f"<{len(mt5_installations)} MT5 installation(s) found.>"
        else:
            return "<No MT5 installations found.>"
    return "<No database available.>"

def explain_empty():
    return empty_string
    

SUB_COMMANDS: list[tuple[str, str | None, Callable[[], None]]] = [
    ['Database', database.callback.__name__, explain_DB], 
    ['MetaTrader 5', metatrader5.callback.__name__, explain_MT5], 
    ['Connect', connect.callback.__name__, explain_empty], 
    ['List', list.callback.__name__, explain_empty], 
    ['Exit nicely', exit.callback.__name__, explain_empty]
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
    SingletonService().put("ApplicationConfig", applicationConfig)
    databaseService = DatabaseService()
    SingletonService().put("DatabaseService", databaseService)

    start_dir=os.getcwd()
    SingletonService().put("start_dir", start_dir)
    accounts = databaseService.accounts()
    SingletonService().put("accounts", accounts)

    while True:
        click.echo(empty_string)
        click.echo(f"Managing {len(accounts)} account(s)")
        if ctx.invoked_subcommand is None:
            choice = interactive_menu(SUB_COMMANDS)
            ctx.invoke(ctx.command.commands[choice])

main.add_command(metatrader5)
main.add_command(connect)
main.add_command(database)
main.add_command(list)
main.add_command(exit)

if __name__ == "__main__":
    main()