import click
from rich.console import Console
from tickdata.commands.describe import describe
from tickdata.commands.append import append
from tickdata.commands.compare import compare
from tickdata.commands.improve import improve
from tickdata.commands.analyze import analyze

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
def tickdata(ctx):
    """Tick data management tool."""
    if ctx.invoked_subcommand is None:
        choice = interactive_menu()
        ctx.invoke(ctx.command.commands[choice])

tickdata.add_command(analyze)
tickdata.add_command(describe)
tickdata.add_command(append)
tickdata.add_command(compare)
tickdata.add_command(improve)