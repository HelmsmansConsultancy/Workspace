import click
from rich.console import Console
from tabular.util.menuutils import interactive_menu

SUB_SUB_COMMANDS: list[tuple[str, str | None]] = [['make', 'make'], ['delete', 'delete'], ['list', 'list'], ['exit', None]]

console = Console()

@click.command()
@click.pass_context
def db(ctx):
    """Status of db."""
    click.echo("Checking database status...")

    
    while True:
        click.echo(f"Managing no DB")
        if ctx.invoked_subcommand is None:
            choice = interactive_menu(SUB_SUB_COMMANDS)
            if choice:
                ctx.invoke(ctx.command.commands[choice])
            else:
                break
    

    