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
from tabular.data.symbols.symbol_info import SymbolInfomation
from tabular.data.orders.pending_order import PendingOrder
from tabular.data.orders.generic_order import GenericOrder
from tabular.util.order.pending_order_util import copyValuesIntoPendingOrder
from tabular.util.order.generic_order_util import copyValuesIntoGenericOrder
from tabular.util.symbols_util import getPairFromName
from MetaTrader5 import TradeOrder

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

@click.command()
def current_pending_orders():
    """ Current Pending order"""
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)

    tradeOrders: list[TradeOrder] = metatrader5Service.getPendingOrders(connected_account.id)
    pendingOrders: list[PendingOrder] = databaseService.getPendingOrders(connected_account.id)

    existingOrders: list[PendingOrder] = []
    newOrders: list[PendingOrder] = []
    removedOrders: list[PendingOrder]
    
    for tradeOrder in tradeOrders:
        order_exists = False
        for pendingOrder in pendingOrders:
            if pendingOrder.ticket == tradeOrder.ticket:
                order_exists = True
                copyValuesIntoPendingOrder(tradeOrder, pendingOrder)
                existingOrders.append(pendingOrder)

        if not order_exists:
            newOrder = PendingOrder()
            newOrder.account_id = connected_account.id
            copyValuesIntoPendingOrder(tradeOrder, newOrder)

            symbol = getPairFromName(tradeOrder.symbol)
            symbolInfomation: SymbolInfomation = databaseService.getSymbolInformationBySymbol(symbol)
            newOrder.symbol_id = symbolInfomation.id
            newOrder.digits = symbolInfomation.digits

            genericOrder: GenericOrder = databaseService.getGenericOrderByStats(newOrder.digits, newOrder.entry, newOrder.sl, newOrder.tp)
            if bool(genericOrder):
                click.echo(f"Found GO {genericOrder}")
                newOrder.generic_id = genericOrder.id
            else:
                genericOrder: GenericOrder = GenericOrder()
                copyValuesIntoGenericOrder(tradeOrder, genericOrder)
                genericOrder.symbol_id = symbolInfomation.id
                genericOrder.digits = symbolInfomation.digits
                click.echo(f"Making GO {genericOrder}")
                genericOrderId = databaseService.addGenericOrder(genericOrder)
                newOrder.generic_id = genericOrderId

            newOrders.append(newOrder)
    
    removedOrders = list(set(pendingOrders) - set(existingOrders))
    databaseService.updatePendingOrders(existingOrders)
    databaseService.addPendingOrders(newOrders)
    databaseService.removePendingOrders(removedOrders)

@click.command()
def list__pending_orders():
    """ List Pending order"""
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT, menuName="Account Orders - Pending")
    pendingOrders: list[PendingOrder] = databaseService.getPendingOrders(connected_account.id)

    if bool(pendingOrders):
        if len(pendingOrders) > 0:
            for order in pendingOrders:
                click.echo(f"{order}")
        else:
            click.echo(f"No Pending orders")
    else:
        click.echo("No database")

PENDING_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [no_active_account, explain_empty, 'Get current orders', current_pending_orders.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'List current orders', list__pending_orders.callback.__name__.replace("_", "-"), ],
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
pending_orders.add_command(list__pending_orders)
