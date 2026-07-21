import click
from typing import Callable 
from rich.console import Console
from tabular.commands.orders_generic.generic_pending_orders import generic_pending_orders
from tabular.commands.orders_generic.generic_open_positions import generic_open_positions
from tabular.util.menu.menus_allow import empty_string, allow_allways, no_active_account
from tabular.util.menu.menus_explain import explain_generic_pending_orders, explain_generic_open_positions, explain_empty, explain_settings
from tabular.util.menu.menus_utils import interactive_menu

console = Console()

ACCOUNT_ORDERS_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [\
    [no_active_account, explain_generic_pending_orders, 'Pending Orders', generic_pending_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_generic_open_positions, 'Open Position', generic_open_positions.callback.__name__.replace("_", "-"), ],
    [allow_allways, explain_empty, 'Return to previous menu', None, ]
]


@click.group(invoke_without_command=True)
@click.pass_context
def menu_generic_orders(ctx):
    choice = None
    while True:
        click.echo(empty_string)
        

        if not bool(choice):
            choice = interactive_menu(ACCOUNT_ORDERS_SUB_COMMANDS, menuName="Generic Orders - Overview")
        
        if bool(choice):
            next_menu = ctx.invoke(ctx.command.commands[choice])
            if bool(next_menu):
                choice = next_menu
            else:
                choice = None  # Reset choice to None after invoking the command
        else:
            return

menu_generic_orders.add_command(generic_pending_orders)
menu_generic_orders.add_command(generic_open_positions)