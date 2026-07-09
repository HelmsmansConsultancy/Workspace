import click
from rich.console import Console
from typing import Callable
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.service.s import S
from tabular.util.menu_utils import interactive_menu, empty_string, explain_empty, allow_allways

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

SYMBOLS_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [allow_allways, explain_empty, 'Return to previous menu', None, ]
]

@click.group()
@click.pass_context
def symbols(ctx: click.Context):
    """Status of symbols."""

    
    choice = None
    while True:
        if choice is None:
            choice = interactive_menu(SYMBOLS_SUB_COMMANDS)

        result = None
        if bool(choice) and bool(choice[1]):
            ctx.invoke(ctx.command.commands[choice[1]])
            result = choice[3] 
            choice = None  # Reset choice to None after invoking the command
        else:
            return result