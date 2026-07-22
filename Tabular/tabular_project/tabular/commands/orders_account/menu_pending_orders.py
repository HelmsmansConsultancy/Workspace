import click
from rich.console import Console
from typing import Callable
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.service.s import S
from tabular.util.menu.menus_allow import empty_string,  no_active_account
from tabular.util.menu.menus_explain import explain_empty
from tabular.util.menu.menus_utils import interactive_menu
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.symbols.specific_symbol_info import SpecificSymbolInfomation
from tabular.data.orders.specific_pending_order import SpecificPendingOrder
from tabular.data.orders.generic_pending_order import GenericPendingOrder
from tabular.util.order.pending_order_util import copyValuesIntoPendingOrder
from tabular.util.order.generic_order_util import copyValuesIntoGenericOrder
from tabular.util.util.symbols_util import getSymbolFromName
from MetaTrader5 import TradeOrder
from tabular.commands.orders_generic.generic_pending_orders import generic_pending_orders

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

@click.command()
def current_pending_orders():
    """ Current Pending order"""
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)

    tradeOrders: list[TradeOrder] = metatrader5Service.getPendingOrders(connected_account.id)
    pendingOrders: list[SpecificPendingOrder] = databaseService.listSpecificPendingOrderByAccount(connected_account.id)

    existingOrders: list[SpecificPendingOrder] = []
    newOrders: list[SpecificPendingOrder] = []
    removedOrders: list[SpecificPendingOrder]
    
    for tradeOrder in tradeOrders:
        order_exists = False
        for pendingOrder in pendingOrders:
            if pendingOrder.ticket == tradeOrder.ticket:
                order_exists = True
                copyValuesIntoPendingOrder(tradeOrder, pendingOrder)
                existingOrders.append(pendingOrder)

        if not order_exists:
            newOrder = SpecificPendingOrder()
            newOrder.account_id = connected_account.id

            copyValuesIntoPendingOrder(tradeOrder, newOrder)
            click.echo(f"Ticket {tradeOrder.ticket}")
            symbol = getSymbolFromName(tradeOrder.symbol)
            symbolInfomation: SpecificSymbolInfomation = databaseService.getSymbolInformationBySymbol(connected_account.id, symbol)
            newOrder.symbol_id = symbolInfomation.id
            newOrder.digits = symbolInfomation.digits
            newOrder.symbol = symbolInfomation.symbol

            genericOrder: GenericPendingOrder = databaseService.getGenericOrderByStats(newOrder.digits, newOrder.entry, newOrder.sl, newOrder.tp)
            if bool(genericOrder):
                click.echo(f"Found GO {genericOrder}")
                newOrder.generic_id = genericOrder.id
            else:
                genericOrder: GenericPendingOrder = GenericPendingOrder()
                
                copyValuesIntoGenericOrder(tradeOrder, genericOrder)
                genericOrder.symbol_id = symbolInfomation.id
                genericOrder.symbol = symbolInfomation.symbol
                genericOrder.digits = symbolInfomation.digits
                click.echo(f"Making GO {genericOrder}")
                genericOrderId = databaseService.saveGenericPendingOrder(genericOrder)
                newOrder.generic_id = genericOrderId

            newOrders.append(newOrder)
    
    removedOrders = list(set(pendingOrders) - set(existingOrders))
    databaseService.updateSpecificPendingOrders(existingOrders)
    databaseService.saveSpecificPendingOrders(newOrders)
    databaseService.removeSpecificPendingOrders(removedOrders)
    return ["", "", generic_pending_orders.callback.__name__.replace("_", "-")]

@click.command()
def list_pending_orders():
    """ List Pending order"""
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    pendingOrders: list[SpecificPendingOrder] = databaseService.listSpecificPendingOrderByAccount(connected_account.id)

    if bool(pendingOrders):
        if len(pendingOrders) > 0:
            for order in pendingOrders:
                click.echo(f"{order}")
        else:
            click.echo(f"No Pending orders")
    else:
        click.echo("No database")

@click.command()
def delete_pending_order():
    """ Delete orders"""
    global databaseService
    global metatrader5Service
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    pendingOrders: list[SpecificPendingOrder] = databaseService.listSpecificPendingOrderByAccount(connected_account.id)
    if len(pendingOrders) == 0:
        click.echo("No Pending Orders found.")
        return
    
    click.echo("Select an order to delete:")
    for index, order in enumerate(pendingOrders, start=1):
        click.echo(f"{index}. {order}")

    choice = click.prompt("Enter the number of the Order to delete", type=int)
    if 1 <= choice <= len(pendingOrders):
        orderToDelete: SpecificPendingOrder = pendingOrders[choice - 1]
        metatrader5Service.deletePendingOrder(orderToDelete.ticket)
        databaseService.deleteSpecificPendingOrder(orderToDelete)
        click.echo(f"Deleted {orderToDelete}")

PENDING_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [no_active_account, explain_empty, 'Get current orders', current_pending_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'List current orders', list_pending_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Delete current order', delete_pending_order.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Return to previous menu', None, ],
]

@click.group()
@click.pass_context
def specific_pending_orders(ctx: click.Context):
    """Status of pending orders."""
    global databaseService
    databaseService = SingletonService().get(S.DATABASE_SERVICE)

    global metatrader5Service
    metatrader5Service = SingletonService().get(S.METATRADER5_SERVICE)

    choice = None
    while True:
        connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
        if bool(connected_account):
            pending_orders = databaseService.listSpecificPendingOrderByAccount(connected_account.id)
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
            choice = interactive_menu(PENDING_SUB_COMMANDS, menuName="Account Orders - Pending")

        result = None
        if bool(choice):
            ctx.invoke(ctx.command.commands[choice])
            choice = None  # Reset choice to None after invoking the command
        else:
            return result

specific_pending_orders.add_command(current_pending_orders)
specific_pending_orders.add_command(list_pending_orders)
specific_pending_orders.add_command(delete_pending_order)
