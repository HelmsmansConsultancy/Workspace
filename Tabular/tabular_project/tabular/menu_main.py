import click
import os
# from pathlib import Path
import sys
from typing import Callable 
from rich.console import Console
from tabular.commands.settings.settings import settings
from tabular.commands.orders_account.menu_closed_deal import trade_deals
from tabular.commands.settings.settings import settings
from tabular.commands.symbols.symbols import symbols
from tabular.commands.orders_account.menu_account_orders import menu_account_orders
from tabular.commands.orders_generic.menu_generic_orders import menu_generic_orders
from tabular.util.menu.menus_allow import empty_string, allow_allways, no_active_account
from tabular.util.menu.menus_explain import explain_symbols, explain_empty, explain_settings_short, explain_generic_orders, explain_specific_orders
from tabular.util.menu.menus_utils import interactive_menu
from tabular.service.s import S
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.data.base.application_config import ApplicationConfig


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
    [allow_allways, explain_settings_short, 'Settings', settings.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_symbols, 'Symbols', symbols.callback.__name__.replace("_", "-"), ],
    [allow_allways, explain_generic_orders, 'Generic Order', menu_generic_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_specific_orders, 'Account Order', menu_account_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Trade Deals', trade_deals.callback.__name__.replace("_", "-"), ],
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
    accounts = databaseService.listAccountConfigs()
    SingletonService().put(S.ACCOUNTS, accounts)

    choice = None
    while True:
        click.echo(empty_string)
        click.echo(f"Managing {len(accounts)} account(s)")
        if not bool(choice):
            choice = interactive_menu(SUB_COMMANDS, menuName="Main Menu")
        
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

main.add_command(settings)
main.add_command(symbols)
main.add_command(menu_generic_orders)
main.add_command(menu_account_orders)
main.add_command(trade_deals)
main.add_command(exit)

if __name__ == "__main__":
    main()