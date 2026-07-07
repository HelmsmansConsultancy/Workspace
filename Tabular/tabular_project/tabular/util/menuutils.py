import click
from typing import Callable 
from rich.console import Console 


console = Console()

empty_string = ""

def interactive_menu(subCommands: list[tuple[str, str | None, Callable[[], str]]]):
    click.echo(empty_string)
    click.echo("What do you want to do?")
    for i, tuple in enumerate(subCommands, 1):
        click.echo(f"  {i}. {tuple[0]} ({tuple[1]}) {tuple[2]() if tuple[2] is not None else ''}")
    idx = click.prompt(
        "Enter number",
        type=click.IntRange(1, len(subCommands))
    )
    return subCommands[idx - 1][1]

