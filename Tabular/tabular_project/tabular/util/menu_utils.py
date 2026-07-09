import click
from typing import Callable 
from rich.console import Console 
from tabular.data.metatrader_config import MetatraderConfig
from tabular.service.singleton_service import SingletonService
from tabular.service.s import S
from tabular.service.database_service import DatabaseService


console = Console()

empty_string = ""


def explain_DB():
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    if databaseService is not None:
        return f"\t\t\t<{databaseService.db_file}>"
    return "\t\t\t<No database available.>"

def explain_accounts():
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
    return message

def explain_empty():
    return empty_string

def explain_MT5():
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
    return message

def interactive_menu(subCommands: list[tuple[str, str | None, Callable[[], str]]]) -> tuple[str, str | None, Callable[[], str]]:
    click.echo(empty_string)
    click.echo("What do you want to do?")
    for i, tuple in enumerate(subCommands, 1):
        click.echo(f"  {i}. {tuple[0]} {tuple[2]() if tuple[2] is not None else ''}")
    idx = click.prompt(
        "Enter number",
        type=click.IntRange(1, len(subCommands))
    )
    return subCommands[idx - 1]

