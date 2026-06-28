import click
import os
from rich.console import Console 


console = Console()



def interactive_menu(subCommands: list[tuple[str, str | None]]):
    click.echo("What do you want to do?")
    for i, tuple in enumerate(subCommands, 1):
        click.echo(f"  {i}. {tuple[0]}")
    idx = click.prompt(
        "Enter number",
        type=click.IntRange(1, len(subCommands))
    )
    return subCommands[idx - 1][1]

