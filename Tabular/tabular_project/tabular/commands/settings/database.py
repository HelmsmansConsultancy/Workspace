import os
import click
import sqlite3
from typing import Callable 
from rich.console import Console
from tabular.service.s import S
from tabular.util.menu.menus_allow import empty_string, allow_allways, no_active_account, no_accounts
from tabular.util.menu.menus_explain import explain_accounts, explain_DB, explain_pending_orders, explain_open_positions, explain_symbols, explain_empty
from tabular.util.menu.menus_utils import interactive_menu
from tabular.util.util.file_utils import determine_new_file
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService

console = Console()
databaseService: DatabaseService = None

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
        rows: int = databaseService.countRows(table)
        click.echo(f"- Table {table} {'\t' if len(table) < 15 else ''}{'\t' if len(table) < 25 else ''}\t {rows} Rows")
    click.echo(empty_string)


DB_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [allow_allways, explain_empty,  'List tables', list_tables.callback.__name__.replace("_", "-"), ], 
    [allow_allways, explain_empty, 'Return to previous menu', None, ]
]

@click.group()
@click.pass_context
def database(ctx: click.Context):
    """Status of database."""
    global databaseService
    databaseService = SingletonService().get("DatabaseService")

    choice = None
    while True:
        """Show basic menu data"""
        size_bytes = os.path.getsize(databaseService.db_file) if databaseService is not None else 0
        click.echo(empty_string)
        click.echo(f"Database file: <{databaseService.db_file}> - Size: {size_bytes:,} bytes")
        if choice is None:
            choice = interactive_menu(DB_SUB_COMMANDS, menuName="Settings - Database")

        result = None
        if bool(choice):
            ctx.invoke(ctx.command.commands[choice])
            choice = None  # Reset choice to None after invoking the command
        else:
            return result
        

#database.add_command(create)
database.add_command(list_tables)
