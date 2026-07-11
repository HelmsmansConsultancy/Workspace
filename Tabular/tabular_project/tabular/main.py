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
from tabular.commands.open_positions import open_positions
from tabular.commands.closed_trades import closed_trades
from tabular.commands.list import list 
from tabular.util.menu_utils import interactive_menu, empty_string, explain_accounts, explain_DB, explain_empty, explain_MT5, allow_allways, no_active_account
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.data.application_config import ApplicationConfig
from tabular.commands.accounts import accounts


console = Console()
applicationConfig: ApplicationConfig = None
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

@click.command()
def exit():
    """Exiting the application."""
    global metatrader5Service

    metatrader5Service.disconnect_mt5()
    click.echo(f"Exiting the application...")
    sys.exit(0)

SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [ allow_allways, explain_DB,'Database', database.callback.__name__, ], 
    [allow_allways, explain_MT5, 'MetaTrader 5', metatrader5.callback.__name__.replace("_", "-"), ], 
    [allow_allways, explain_accounts, 'Accounts', accounts.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Pending Orders', pending_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Open Position', open_positions.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Closed Trades', closed_trades.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Symbols', symbols.callback.__name__.replace("_", "-"), ], 
    [allow_allways, explain_empty, 'Exit nicely', exit.callback.__name__.replace("_", "-"), ]
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
    global menuService

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
        if bool(choice):
            next_menu = ctx.invoke(ctx.command.commands[choice])
            if bool(next_menu):
                click.echo(f"Next menu: {next_menu}")
                ctx.invoke(ctx.command.commands[next_menu])
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
main.add_command(open_positions)
main.add_command(closed_trades)
main.add_command(exit)

if __name__ == "__main__":
    main()