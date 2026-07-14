import click
from typing import Callable 
from rich.console import Console
from tabular.commands.orders_account.pending_orders import pending_orders
from tabular.commands.orders_account.open_positions import open_positions
from tabular.commands.closed_deal import trade_deals
from tabular.commands.list import list 
from tabular.util.menu.menus_allow import empty_string, allow_allways, no_active_account
from tabular.util.menu.menus_explain import explain_pending_orders, explain_open_positions, explain_symbols, explain_empty, explain_settings
from tabular.util.menu.menus_utils import interactive_menu
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.data.application_config import ApplicationConfig
from tabular.commands.settings.settings import settings

console = Console()

ACCOUNT_ORDERS_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [\
    [no_active_account, explain_pending_orders, 'Pending Orders', pending_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_open_positions, 'Open Position', open_positions.callback.__name__.replace("_", "-"), ],
    [allow_allways, explain_empty, 'Return to previous menu', None, ]
]


@click.group(invoke_without_command=True)
@click.pass_context
def generic_orders(ctx):
    choice = None
    while True:
        click.echo(empty_string)
        

        if not bool(choice):
            choice = interactive_menu(ACCOUNT_ORDERS_SUB_COMMANDS)
        
        if bool(choice):
            next_menu = ctx.invoke(ctx.command.commands[choice])
            if bool(next_menu):
                choice = next_menu
            else:
                choice = None  # Reset choice to None after invoking the command
        else:
            return

generic_orders.add_command(pending_orders)
generic_orders.add_command(open_positions)