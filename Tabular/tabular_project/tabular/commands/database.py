import os

import click
import sqlite3
from typing import Callable 
from rich.console import Console
from tabular.util.menuutils import interactive_menu, empty_string
from tabular.util.fileutils import determine_new_file
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService

console = Console()
databaseService: DatabaseService = None

def explain_empty():
    return empty_string
    

DB_SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str]]] = [
#    ['Create / select', 'create', explain_empty], 
#    ['delete', 'delete', explain_empty], 
    ['List tables', 'list', explain_empty], 
    ['Return to previous menu', None, explain_empty]
]

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


@click.command()
def list():
    """List all databases."""
    global databaseService
    tables: list[str] = databaseService.listTables()
    click.echo(empty_string)
    click.echo("Tables in the database:")
    for table in tables:
        click.echo(f"- {table}")
    click.echo(empty_string)



@click.group()
@click.pass_context
def database(ctx: click.Context):
    """Status of db."""
    global databaseService

    databaseService = SingletonService().get("DatabaseService")
    size_bytes = os.path.getsize(databaseService.db_file) if databaseService is not None else 0
    click.echo(empty_string)
    click.echo(f"Database file: <{databaseService.db_file}> - Size: {size_bytes:,} bytes")

    while True:
        if ctx.invoked_subcommand is None:
            choice = interactive_menu(DB_SUB_COMMANDS)
            if choice:
                ctx.invoke(ctx.command.commands[choice])
            else:
                break

database.add_command(create)
database.add_command(list)
