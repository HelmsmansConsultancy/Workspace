import click
from rich.console import Console
from typing import Callable
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.service.s import S
from tabular.util.menu_utils import interactive_menu, empty_string

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

def explain_empty():
    return empty_string
    

SYMBOLS_SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str], str | None]] = [
    ['Return to previous menu', None, explain_empty, None]
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