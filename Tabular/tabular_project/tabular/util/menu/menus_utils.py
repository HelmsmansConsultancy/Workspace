import click
from typing import Callable 
from rich.console import Console 
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.settings.account_config import AccountConfig
from tabular.service.singleton_service import SingletonService
from tabular.service.s import S
from tabular.service.database_service import DatabaseService


console = Console()

empty_string = ""

def interactive_menu(subCommands: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]], menuName: str = None) -> str:
    click.echo(empty_string)
    click.echo(f"{menuName} - What do you want to do?")
    for i, tuple in enumerate(subCommands, 1):
        enabled = tuple[0]()
        line = f"  {i}. {tuple[2]} {tuple[1](enabled) if tuple[1] is not None else ''}"
        if enabled:
            click.echo(line)
        else:
            click.echo(click.style(line + " (disabled)", dim=True, fg="bright_black"))
    idx = click.prompt(
        "Enter number",
        type=click.IntRange(1, len(subCommands))
    )
    return subCommands[idx - 1][3]

