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

ACCOUNT_SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str, str | None]]] = [
#    ['Create / select', 'create', explain_empty, None], 
#    ['delete', 'delete', explain_empty, None], 
    ['Return to previous menu', None, explain_empty, None]
]

@click.group()
@click.pass_context
def accounts(ctx: click.Context):
    """Status of db."""
    global databaseService
    databaseService = SingletonService().get(S.DATABASE_SERVICE)

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
        
        result = None
        if bool(choice) and bool(choice[1]):
            click.echo(f"Invoking command: {choice}")
            ctx.invoke(ctx.command.commands[choice[1]])
            result = choice[3]
            choice = None  # Reset choice to None after invoking the command
        else:
            click.echo("accounts.py: Back to the previous menu")
            return result