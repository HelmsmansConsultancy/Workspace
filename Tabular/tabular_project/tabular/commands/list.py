import click
from rich.console import Console
from ..service.singleton_service import SingletonService
from ..data.account_config import AccountConfig


console = Console()

@click.command()
def list():
    """Connect to a data source."""
    accounts: list[AccountConfig] = SingletonService().get("accounts")
    click.echo(f"List {len(accounts)} accounts")
    for account in accounts:
        click.echo(f"Account: {account.backend.firm} {account.id} of type {account.type} with Size {account.money.base} {account.money.currency}")


