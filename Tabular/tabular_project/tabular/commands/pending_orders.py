import click
from rich.console import Console
from typing import Callable
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.service.s import S
from tabular.util.menus_allow import empty_string, allow_allways, no_active_account
from tabular.util.menus_explain import explain_accounts, explain_DB, explain_pending_orders, explain_open_positions, explain_symbols, explain_empty
from tabular.util.menus_utils import interactive_menu
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.pending_order import PendingOrder
from tabular.util.orders_util import copyValuesInto
from MetaTrader5 import TradeOrder

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

@click.command()
def current_pending_orders():
    """ Current Pending order"""
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    tradeOrders: list[TradeOrder] = metatrader5Service.getPendingOrders(connected_account.id)
    click.echo(f"Gotten {len(tradeOrders)} trades")
    pendingOrders: list[PendingOrder] = databaseService.getPendingOrders(connected_account.id)
    existingOrders: list[PendingOrder] = []
    newOrders: list[PendingOrder] = []
    removedOrders: list[PendingOrder]
    for tradeOrder in tradeOrders:
        order_exists = False
        for pendingOrder in pendingOrders:
            if pendingOrder.ticket == tradeOrder.ticket:
                order_exists = True
                copyValuesInto(tradeOrder, pendingOrder)
                existingOrders.append(pendingOrder)

        if not order_exists:
            newOrder = PendingOrder()
            newOrder.account_id = connected_account.id
            copyValuesInto(tradeOrder, newOrder)
            newOrders.append(newOrder)
    
    removedOrders = list(set(pendingOrders) - set(existingOrders))
    databaseService.updatePendingOrders(existingOrders)
    databaseService.addPendingOrders(newOrders)
    databaseService.removePendingOrders(removedOrders)

PENDING_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [no_active_account, explain_empty, 'Get current orders', current_pending_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Return to previous menu', None, ],
]

@click.group()
@click.pass_context
def pending_orders(ctx: click.Context):
    """Status of pending orders."""
    global databaseService
    databaseService = SingletonService().get(S.DATABASE_SERVICE)

    global metatrader5Service
    metatrader5Service = SingletonService().get(S.METATRADER5_SERVICE)

    choice = None
    while True:
        connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
        if bool(connected_account):
            pending_orders = databaseService.getPendingOrders(connected_account.id);
            if len(pending_orders) > 0:
                click.echo(empty_string)
                for pending_order in pending_orders:
                    click.echo(f"{pending_order}")
            else :
                click.echo(f"No pending order")
        else :
            click.echo(f"No account connected")
        click.echo(empty_string)

        if choice is None:
            choice = interactive_menu(PENDING_SUB_COMMANDS)

        result = None
        if bool(choice):
            ctx.invoke(ctx.command.commands[choice])
            choice = None  # Reset choice to None after invoking the command
        else:
            return result

pending_orders.add_command(current_pending_orders)
