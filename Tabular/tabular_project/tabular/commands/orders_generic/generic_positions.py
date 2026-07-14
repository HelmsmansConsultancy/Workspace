import click
from rich.console import Console
from typing import Callable
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.service.s import S
from tabular.util.menu.menus_allow import empty_string, no_active_account
from tabular.util.menu.menus_explain import explain_empty
from tabular.util.menu.menus_utils import interactive_menu
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.open_position import OpenPosition
from tabular.util.order.open_position_util import copyValuesInto
from MetaTrader5 import TradeOrder

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

@click.command()
def current_open_positions():
    """ Current Pending order"""
    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    tradeOrders: list[TradeOrder] = metatrader5Service.getTradeDeals(connected_account.id)
    click.echo(f"Gotten {len(tradeOrders)} trades")
    openPositions: list[OpenPosition] = databaseService.getTradeDeals(connected_account.id)
    existingOrders: list[OpenPosition] = []
    newPositions: list[OpenPosition] = []
    removedPositions: list[OpenPosition]
    for tradeOrder in tradeOrders:
        order_exists = False
        for openPosition in openPositions:
            if openPosition.ticket == tradeOrder.ticket:
                order_exists = True
                copyValuesInto(tradeOrder, openPosition)
                existingOrders.append(openPosition)

        if not order_exists:
            newOrder = OpenPosition()
            newOrder.account_id = connected_account.id
            copyValuesInto(tradeOrder, newOrder)
            newPositions.append(newOrder)
    
    removedPositions = list(set(openPositions) - set(existingOrders))
    databaseService.updateOpenPositions(existingOrders)
    databaseService.addOpenPositions(newPositions)
    databaseService.removeOpenPositions(removedPositions)

OPEN_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [no_active_account, explain_empty, 'Get current positions', current_open_positions.callback.__name__.replace("_", "-"), ],
    [no_active_account, explain_empty, 'Return to previous menu', None, ],
]


@click.group()
@click.pass_context
def open_positions(ctx: click.Context):
    """Status of pending orders."""
    global databaseService
    databaseService = SingletonService().get(S.DATABASE_SERVICE)

    global metatrader5Service
    metatrader5Service = SingletonService().get(S.METATRADER5_SERVICE)

    choice = None
    while True:
        connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
        if bool(connected_account):
            openPositions = databaseService.getTradeDeals(connected_account.id);
            if len(openPositions) > 0:
                click.echo(empty_string)
                for openPosition in openPositions:
                    click.echo(f"{openPosition}")
            else :
                click.echo(f"No open position")
        else :
            click.echo(f"No account connected")
        click.echo(empty_string)

        if choice is None:
            choice = interactive_menu(OPEN_SUB_COMMANDS)

        result = None
        if bool(choice):
            ctx.invoke(ctx.command.commands[choice])
            choice = None  # Reset choice to None after invoking the command
        else:
            return result
        
open_positions.add_command(current_open_positions)