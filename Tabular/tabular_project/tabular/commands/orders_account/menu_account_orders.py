import click
from pathlib import Path
from typing import Callable 
from rich.console import Console
from tabular.commands.orders_account.menu_pending_orders import pending_orders
from tabular.commands.orders_account.menu_open_positions import open_positions
from tabular.commands.orders_account.menu_closed_deal import trade_deals
from tabular.util.menu.menus_allow import empty_string, allow_allways, no_active_account
from tabular.util.menu.menus_explain import explain_pending_orders, explain_open_positions, explain_symbols, explain_empty, explain_settings
from tabular.util.menu.menus_utils import interactive_menu

console = Console()

ACCOUNT_ORDERS_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [\
    [no_active_account, explain_pending_orders, 'Pending Orders', pending_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_open_positions, 'Open Position', open_positions.callback.__name__.replace("_", "-"), ],
    [allow_allways, explain_empty, 'Return to previous menu', None, ]
]


@click.group(invoke_without_command=True)
@click.pass_context
def account_orders(ctx):
    choice = None
    while True:
        click.echo(empty_string)
        

        if not bool(choice):
            choice = interactive_menu(ACCOUNT_ORDERS_SUB_COMMANDS, menuName="Account Orders - Overview")
        
        if bool(choice):
            next_menu: list[str] = ctx.invoke(ctx.command.commands[choice])
            click.echo(f"Next_menu {Path(__file__).name}: {next_menu}")
            if bool(next_menu):
                if len(next_menu) > 1:
                    return next_menu[1:]
                else:
                    choice = next_menu[0]
            else:
                choice = None  # Reset choice to None after invoking the command
        else:
            return

account_orders.add_command(pending_orders)
account_orders.add_command(open_positions)