import click
from rich.console import Console
from ..service.singleton_service import SingletonService
from ..data.account_config import AccountConfig
from ..util.fileutils import list_files

console = Console()


def interactive_menu(accounts: list[AccountConfig]) -> AccountConfig:
    click.echo("Choose which account...")
    for i, account in enumerate(accounts, 1):
        click.echo(f"  {i}. {account.id}")
    idx = click.prompt(
        "Enter number",
        type=click.IntRange(1, len(accounts))
    )
    return idx - 1

@click.command()
def connect():
    accounts: list[AccountConfig] = SingletonService().get("accounts")
    idx = 0
    """Connect to a data source."""        
    if len(accounts) == 0:
        click.echo("No accounts found in the configuration.")
        return
    if len(accounts) == 0:
        idx = interactive_menu(accounts)


    account = accounts[idx]
    click.echo(f"Connecting to: {account.backend.firm} {account.id} {account.path} of type {account.type} with Size {account.money.base} {account.money.currency}")
    list_files(account.path)

