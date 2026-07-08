import os
import click
import sqlite3
from typing import Callable 
from rich.console import Console
from tabular.service.s import S
from tabular.util.menuutils import interactive_menu, empty_string
from tabular.util.fileutils import determine_new_file
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService

console = Console()
databaseService: DatabaseService = None

def explain_empty():
    return empty_string
    

@click.command()
def create():
    """Create a new database."""
    click.echo("Creating a new database...")
    start_dir = SingletonService().get(S.START_DIR)
    db_file = determine_new_file(start_dir)
    # Ensure .db extension
    if not db_file.endswith(".db"):
        db_file += ".db"

    # This creates the file on disk
    conn = sqlite3.connect(db_file)
    conn.close()
    click.echo(f"File: {db_file} created")
    # Implement the logic to create a new database here


@click.command()
def list_tables():
    """List all databases."""
    global databaseService
    tables: list_tables[str] = databaseService.listTables()
    click.echo(empty_string)
    click.echo("Tables in the database:")
    for table in tables:
        click.echo(f"- {table}")
    click.echo(empty_string)


DB_SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str, str | None]]] = [
#    ['Create / select', 'create', explain_empty, None], 
#    ['delete', 'delete', explain_empty, None], 
    ['List tables', list_tables.callback.__name__.replace("_", "-"), explain_empty, None], 
    ['Return to previous menu', None, explain_empty, None]
]

@click.group()
@click.pass_context
def database(ctx: click.Context):
    """Status of db."""
    global databaseService

    databaseService = SingletonService().get("DatabaseService")
    size_bytes = os.path.getsize(databaseService.db_file) if databaseService is not None else 0
    click.echo(empty_string)
    click.echo(f"Database file: <{databaseService.db_file}> - Size: {size_bytes:,} bytes")

    choice = None
    while True:
        if choice is None:
            choice = interactive_menu(DB_SUB_COMMANDS)

        result = None
        if bool(choice) and bool(choice[1]):
            click.echo(f"Invoking command: {choice}")
            ctx.invoke(ctx.command.commands[choice[1]])
            result = choice[3] 
            choice = None  # Reset choice to None after invoking the command
        else:
            click.echo("database.py: Back to the previous menu")
            return result
        

#database.add_command(create)
database.add_command(list_tables)
