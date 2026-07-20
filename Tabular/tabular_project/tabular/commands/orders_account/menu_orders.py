import click
from rich.console import Console
from typing import Callable
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.service.s import S
from tabular.util.menu.menus_allow import empty_string, allow_allways, no_active_account
from tabular.util.menu.menus_explain import explain_empty
from tabular.util.menu.menus_utils import interactive_menu
from tabular.data.settings.metatrader_config import MetatraderConfig

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

OPEN_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [no_active_account, explain_empty, 'Return to previous menu', None, ],
]


@click.group()
@click.pass_context
def orders(ctx: click.Context):
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
        
orders.add_command(current_open_positions)