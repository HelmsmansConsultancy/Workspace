import click
from decimal import Decimal, ROUND_HALF_UP
import MetaTrader5 as meta_trader_5
from MetaTrader5 import AccountInfo 
from typing import Callable 
from rich.console import Console
from tabular.service.s import S
from tabular.util.menu_utils import interactive_menu, empty_string, explain_empty, allow_allways
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.data.account_config import AccountConfig
from tabular.data.account_status import AccountStatus
from tabular.data.account_metatrader_connection import AccountMetatraderConnection
from tabular.data.metatrader_config import MetatraderConfig
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.commands.pending_orders import pending_orders

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

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
            currency=account_info.currency,
            company=account_info.company,
            leverage=account_info.leverage,
            login=account_info.login,
            name=account_info.name,
            server=account_info.server,
            trade_mode=account_info.trade_mode
        )
        databaseService.addAccount(new_account_config)
        new_account_status = AccountStatus(
            account_id=new_account_config.id,
            balance=Decimal(account_info.balance).quantize(S.CENT, rounding=ROUND_HALF_UP),
            equity=Decimal(account_info.equity).quantize(S.CENT, rounding=ROUND_HALF_UP),
            profit=Decimal(account_info.profit).quantize(S.CENT, rounding=ROUND_HALF_UP)    ,
            trade_allowed=account_info.trade_allowed,
            trade_expert=account_info.trade_expert,
        )
        databaseService.addAccountStatus(new_account_status)
        new_account_metatrader_connection = AccountMetatraderConnection(
            new_account_config.id,
            connected_mt5.id
        )
        databaseService.addAccountMetatraderConnection(new_account_metatrader_connection)
        SingletonService().put(S.CONNECTED_ACCOUNT, new_account_config)
        click.echo(f"New account with login {new_account_config.login} and company {new_account_config.company} added to the database.")

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

@click.command()
def connect_account():
    """Connect account."""
    
    account_configs: list[AccountConfig] = databaseService.list_account_configs()
    if len(account_configs) == 0:
        click.echo("No Account Configs found.")
        return

    click.echo("Select an Account to connect to:")
    for index, mt5 in enumerate(account_configs, start=1):
        click.echo(f"{index}. {mt5}")

    choice = click.prompt("Enter the number of the Account to connect to", type=int)
    if 1 <= choice <= len(account_configs):
        account_to_connect: AccountConfig = account_configs[choice - 1]
        #updated_mt5_config = metatrader5Service.connect_mt5(mt5_to_connect)
        #databaseService.updateMetatrader(account_to_connect)
        SingletonService().put(S.CONNECTED_ACCOUNT, account_to_connect)
    else:
        click.echo("Invalid choice. No MT5 installation connected.")
    return pending_orders.callback.__name__.replace("_", "-")


ACCOUNT_SUB_COMMANDS: list[tuple[str, str | None, Callable[[bool], str], Callable[[], bool]]] = [
    ['Create account from MT5', create_account_mt5.callback.__name__.replace("_", "-"), explain_empty, allow_allways], 
    ['List accounts', list_accounts.callback.__name__.replace("_", "-"), explain_empty, allow_allways], 
    ['Connect account', connect_account.callback.__name__.replace("_", "-"), explain_empty, allow_allways], 
    ['Return to previous menu', None, explain_empty, allow_allways]
]

@click.group()
@click.pass_context
def accounts(ctx: click.Context):
    """Status of db."""
    global databaseService
    global metatrader5Service
    databaseService = SingletonService().get(S.DATABASE_SERVICE)
    metatrader5Service = SingletonService().get(S.METATRADER5_SERVICE)

    choice = None
    while True:
        account_configs: list[AccountConfig] = databaseService.list_account_configs()
        account_states: list[AccountStatus] = databaseService.list_account_states()
        click.echo(empty_string)
        click.echo("Accounts:")
        if bool(account_configs) and len(account_configs) > 0:
            for account_config in account_configs:
                click.echo(f"- {account_config!r}")
            if bool(account_states) and len(account_states) > 0:
                click.echo(empty_string)
                click.echo("Account States:")
                for account_state in account_states:
                    click.echo(f"- {account_state!r}")
        else:
            click.echo("No Account Configs found.")
        click.echo(empty_string)

        if choice is None:
            choice = interactive_menu(ACCOUNT_SUB_COMMANDS)

        result = None
        if bool(choice) and bool(choice[1]):
            next_menu = ctx.invoke(ctx.command.commands[choice[1]])
            if bool(next_menu):
                click.echo(f"Next menu: {next_menu}")
                return next_menu
            result = choice[3]
            choice = None  # Reset choice to None after invoking the command
        else:
            return result

accounts.add_command(create_account_mt5)
accounts.add_command(list_accounts)
accounts.add_command(connect_account)
