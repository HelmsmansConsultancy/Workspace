import click
import MetaTrader5 as meta_trader_5
from MetaTrader5 import AccountInfo 
from typing import Callable 
from rich.console import Console
from tabular.service.s import S
from tabular.util.menuutils import interactive_menu, empty_string
from tabular.util.fileutils import determine_new_file
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.data.account_config import AccountConfig
from tabular.data.metatrader_config import MetatraderConfig

console = Console()
databaseService: DatabaseService = None

def explain_empty():
    return empty_string

@click.command()
def create_account_mt5():
    """Create a new account from MT5."""
    click.echo("Creating a new account from MT5...")
    # Implement the logic to create a new account from MT5 here
    connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if connected_mt5 is None:
        click.echo("No connected MT5 installation found. Please connect to an MT5 installation first.")
        return
    account_info: AccountInfo = meta_trader_5.account_info()
    account_config = databaseService.find_account_by_login_and_company(account_info.login, account_info.company)
    if bool(account_config):
        click.echo(f"Account with login {account_info.login} and company {account_info.company} already exists in the database.")
        return
    else:
        new_account_config = AccountConfig(
            login=account_info.login,
            company=account_info.company,
            name=account_info.name,
            server=account_info.server,
            currency=account_info.currency,
        )
        databaseService.addAccount(new_account_config)
        click.echo(f"New account with login {account_info.login} and company {account_info.company} added to the database.")

@click.command()
def list_accounts():
    """List all accounts."""
    global databaseService
    account_configs: list[AccountConfig] = databaseService.list_account_configs()
    click.echo(empty_string)
    click.echo("Accounts in the database:")
    if bool(account_configs) and len(account_configs) > 0:
        for account_config in account_configs:
            click.echo(f"- {account_config}")
    else:
        click.echo("No Account Configs found.")
    click.echo(empty_string)

ACCOUNT_SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str | None]]] = [
    ['Create account from MT5', create_account_mt5.callback.__name__.replace("_", "-"), explain_empty, None], 
    ['List accounts', list_accounts.callback.__name__.replace("_", "-"), explain_empty, None], 
    ['Return to previous menu', None, explain_empty, None]
]

@click.group()
@click.pass_context
def accounts(ctx: click.Context):
    """Status of db."""
    global databaseService
    databaseService = SingletonService().get(S.DATABASE_SERVICE)

    choice = None
    while True:
        account_configs = databaseService.list_account_configs()
        click.echo(empty_string)
        click.echo("Accounts:")
        if bool(account_configs) and len(account_configs) > 0:
            for account_config in account_configs:
                click.echo(f"- {account_config}")
        else:
            click.echo("No Account Configs found.")
        click.echo(empty_string)

        if choice is None:
            choice = interactive_menu(ACCOUNT_SUB_COMMANDS)

        result = None
        if bool(choice) and bool(choice[1]):
            ctx.invoke(ctx.command.commands[choice[1]])
            result = choice[3]
            choice = None  # Reset choice to None after invoking the command
        else:
            return result

accounts.add_command(create_account_mt5)
accounts.add_command(list_accounts)
