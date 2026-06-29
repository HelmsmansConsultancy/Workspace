import click
import sqlite3
from rich.console import Console
from tabular.util.menuutils import interactive_menu
from tabular.util.fileutils import determine_new_file
from tabular.service.singleton_service import SingletonService

SUB_SUB_COMMANDS: list[tuple[str, str | None]] = [
    ['Create / select', 'create'], 
    ['delete', 'delete'], 
    ['list', 'list'], 
    ['Return to previous menu', None]
]

console = Console()

@click.command()
def create():
    """Create a new database."""
    click.echo("Creating a new database...")
    start_dir = SingletonService().get("start_dir")
    db_file = determine_new_file(start_dir)
    # Ensure .db extension
    if not db_file.endswith(".db"):
        db_file += ".db"

    # This creates the file on disk
    conn = sqlite3.connect(db_file)
    conn.close()
    click.echo(f"File: {db_file} created")
    # Implement the logic to create a new database here



@click.group()
#@click.command()
@click.pass_context
def db(ctx: click.Context):
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

db.add_command(create)
