import click
from rich.console import Console
from tabular.commands.describe import describe
from tabular.commands.append import append
from tabular.commands.compare import compare
from tabular.commands.improve import improve
from tabular.commands.analyze import analyze

SUBCOMMANDS = ['analyze','describe', 'append', 'compare', 'improve']

console = Console()

def interactive_menu():
    click.echo("What do you want to do?")
    for i, name in enumerate(SUBCOMMANDS, 1):
        click.echo(f"  {i}. {name}")
    idx = click.prompt(
        "Enter number",
        type=click.IntRange(1, len(SUBCOMMANDS))
    )
    return SUBCOMMANDS[idx - 1]

@click.group(invoke_without_command=True)
@click.pass_context
def tabular(ctx):
    """Tabular MT5 data management tool."""
    if ctx.invoked_subcommand is None:
        choice = interactive_menu()
        ctx.invoke(ctx.command.commands[choice])

tabular.add_command(analyze)
tabular.add_command(describe)
tabular.add_command(append)
tabular.add_command(compare)
tabular.add_command(improve)