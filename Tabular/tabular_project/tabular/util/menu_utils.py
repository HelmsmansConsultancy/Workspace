import click
from typing import Callable 
from rich.console import Console 
from tabular.data.metatrader_config import MetatraderConfig
from tabular.service.singleton_service import SingletonService
from tabular.service.s import S
from tabular.service.database_service import DatabaseService


console = Console()

empty_string = ""


def explain_DB(enabled:bool = True):
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    message: None
    if databaseService is not None:
        message = f"\t\t\t<{databaseService.db_file}>"
    message = "\t\t\t<No database available.>"
    if not enabled:
        message += " (Disabled)"
    return message

def explain_accounts(enabled:bool = True):
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    message = ""
    if databaseService is not None:
        accounts = databaseService.countAccounts()
        if accounts > 0:
            message = f"\t\t\t<{accounts} account(s)>"
        else:
            message = "\t\t\t<No accounts>"
    else:
        message = "\t\t\t<No database available.>"

    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    if bool(connected_account):
        message += f" <Connected with: {connected_account.name}>"
    else:
        message += " <Not connected>"
    
    if not enabled:
        message += " (Disabled)"
    return message

def allow_allways():
    return True

def allow_never():
    return False

def explain_empty(enabled:bool = True):
    return empty_string

def explain_MT5(enabled:bool = True):
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    message = ""
    if databaseService is not None:
        mt5_installations = databaseService.countMetatraders()
        if mt5_installations > 0:
            message = f"\t\t<{mt5_installations} MT5 installation(s)>"
        else:
            message = "\t\t<No MT5 installations found.>"
    else:
        message = "\t\t<No database available.>"

    connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if bool(connected_mt5):
        message += f" <Connected to: {connected_mt5.name}>"
    else:
        message += " <Not connected>"
    
    if not enabled:
        message += " (Disabled)"
    return message

def interactive_menu(subCommands: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]]) -> str:
    click.echo(empty_string)
    click.echo("What do you want to do?")
    for i, tuple in enumerate(subCommands, 1):
        enabled = tuple[0]()
        line = f"  {i}. {tuple[2]} {tuple[1](enabled) if tuple[1] is not None else ''}"
        if enabled:
            click.echo(line)
        else:
            click.echo(click.style(line + " (disabled)", dim=True, fg="bright_black"))
    idx = click.prompt(
        "Enter number",
        type=click.IntRange(1, len(subCommands))
    )
    return subCommands[idx - 1][3]

