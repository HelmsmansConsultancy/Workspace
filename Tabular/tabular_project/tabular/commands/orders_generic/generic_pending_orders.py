import click
# from pathlib import Path
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
from tabular.data.orders.generic_pending_order import GenericPendingOrder
from MetaTrader5 import  TradeOrder
from tabular.data.orders.specific_pending_order import SpecificPendingOrder
from tabular.util.order.pending_order_util import copyValuesIntoPendingOrder
from tabular.util.util.symbols_util import getSymbolFromName
from tabular.data.symbols.symbol_info import SymbolInfomation

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

@click.command()
def list_generic_orders():
    """ List Pending order"""
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    genericOrders: list[GenericPendingOrder] = databaseService.getGenericOrders()

    if bool(genericOrders):
        if len(genericOrders) > 0:
            for order in genericOrders:
                click.echo(f"{order}")
        else:
            click.echo(f"No Pending orders")
    else:
        click.echo("No database")

@click.command()
def copy_generic_orders():
    """ Copy a generic pending order"""
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    global databaseService
    global metatrader5Service

    genericOrders: list[GenericPendingOrder] = databaseService.getGenericOrders()
    if len(genericOrders) == 0:
        click.echo("No Generic Orders found.")
        return

    click.echo("Select an Order to Copy:")
    for index, order in enumerate(genericOrders, start=1):
        click.echo(f"{index}. {order}")

    choice = click.prompt("Enter the number of the Account to connect to", type=int)
    if 1 <= choice <= len(genericOrders):
        orderToPlace: GenericPendingOrder = genericOrders[choice - 1]
        databaseService.getSymbolInformationBySymbol(connected_account.id, orderToPlace.symbol)
        
        tradeOrder: TradeOrder = metatrader5Service.placePendingOrder(orderToPlace)
        
        newOrder = SpecificPendingOrder()
        newOrder.generic_id = orderToPlace.id
        newOrder.account_id = connected_account.id

        copyValuesIntoPendingOrder(tradeOrder, newOrder)

        symbol = getSymbolFromName(tradeOrder.symbol)
        symbolInfomation: SymbolInfomation = databaseService.getSymbolInformationBySymbol(connected_account.id, symbol)
        newOrder.symbol_id = symbolInfomation.id
        newOrder.digits = symbolInfomation.digits
        newOrder.symbol = symbolInfomation.symbol

        databaseService.addPendingOrders([newOrder])


@click.command()
def delete_pending_order():
    """ Delete orders"""
    global databaseService
    global metatrader5Service
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    pendingOrders: list[GenericPendingOrder] = databaseService.getGenericPendingOrders()
    if len(pendingOrders) == 0:
        click.echo("No Pending Orders found.")
        return
    
    click.echo("Select an order to delete:")
    for index, order in enumerate(pendingOrders, start=1):
        click.echo(f"{index}. {order}")

    choice = click.prompt("Enter the number of the Order to delete", type=int)
    if 1 <= choice <= len(pendingOrders):
        orderToDelete: GenericPendingOrder = pendingOrders[choice - 1]
        databaseService.deleteSpecificPendingOrder(orderToDelete)
        click.echo(f"Deleted {orderToDelete}")

PENDING_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [no_active_account, explain_empty, 'List generic orders', list_generic_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Copy generic orders', copy_generic_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Return to previous menu', None, ],
]

@click.group()
@click.pass_context
def generic_pending_orders(ctx: click.Context):
    """Status of pending orders."""
    global databaseService
    databaseService = SingletonService().get(S.DATABASE_SERVICE)

    global metatrader5Service
    metatrader5Service = SingletonService().get(S.METATRADER5_SERVICE)

    choice = None
    while True:
        connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
        if bool(connected_account):
            generic_orders = databaseService.getGenericOrders();
            if len(generic_orders) > 0:
                click.echo(empty_string)
                for generic_order in generic_orders:
                    click.echo(f"{generic_order}")
            else :
                click.echo(f"No pending order")
        else :
            click.echo(f"No account connected")
        click.echo(empty_string)

        if choice is None:
            choice = interactive_menu(PENDING_SUB_COMMANDS, menuName="Generic Orders - Pending")

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
        else:
            return

generic_pending_orders.add_command(list_generic_orders)
generic_pending_orders.add_command(copy_generic_orders)
