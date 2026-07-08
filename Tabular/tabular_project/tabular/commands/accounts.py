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

ACCOUNT_SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str]]] = [
#    ['Create / select', 'create', explain_empty], 
#    ['delete', 'delete', explain_empty], 
    ['Return to previous menu', None, explain_empty]
]

@click.group()
@click.pass_context
def accounts(ctx: click.Context):
    """Status of db."""
    global databaseService
    databaseService = SingletonService().get("DatabaseService")

    account_configs = databaseService.list_account_configs()
    click.echo(empty_string)
    click.echo("Accounts:")
    if bool(account_configs) and len(account_configs) > 0:
        for account_config in account_configs:
            click.echo(f"- {account_config}")
    else:
        click.echo("No Account Configs found.")
    click.echo(empty_string)

    choice = None
    while True:
        if choice is None:
            choice = interactive_menu(ACCOUNT_SUB_COMMANDS)
        if bool(choice):
            ctx.invoke(ctx.command.commands[choice])
        else:
            click.echo("accounts.py: Back to the previous menu")
            break