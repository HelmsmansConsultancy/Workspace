import click
import os
# from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from MetaTrader5 import AccountInfo
from typing import Callable 
from rich.console import Console
from tabular.service.s import S
from tabular.util.menu.menus_allow import empty_string, allow_allways, no_accounts, no_active_metatrader
from tabular.util.menu.menus_explain import explain_empty
from tabular.util.menu.menus_utils import interactive_menu
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.data.settings.account_config import AccountConfig
from tabular.data.settings.account_status import AccountStatus
from tabular.data.settings.account_metatrader_connection import AccountMetatraderConnection
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.commands.symbols.symbols import symbols
from getpass import getpass

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None

@click.command()
def list_accounts():
    """List all accounts."""
    click.echo(empty_string)
    connected_account = SingletonService().get(S.CONNECTED_ACCOUNT)
    if bool(connect_account):
        click.echo(f"Connected to {connected_account}")
    else:
        click.echo(f"Currently not connected with any account")

@click.command()
def create_account_mt5():
    """Create a new account from MT5."""
    click.echo("Creating a new account from MT5...")
    # Implement the logic to create a new account from MT5 here
    connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if connected_mt5 is None:
        click.echo("No connected MT5 installation found. Please connect to an MT5 installation first.")
        return
    account_info: AccountInfo = metatrader5Service.getAccountInfo()
    account_config = databaseService.find_account_by_login_and_company(account_info.login, account_info.company)
    if bool(account_config):
        click.echo(f"Account with login {account_info.login} and company {account_info.company} already exists in the database.")
        return
    else:
        account_config = AccountConfig(
            currency=account_info.currency,
            company=account_info.company,
            leverage=account_info.leverage,
            account_login=account_info.login,
            name=account_info.name,
            password=None,
            server=account_info.server,
            trade_mode=account_info.trade_mode
        )
        databaseService.saveAccountConfig(account_config)
        account_status = AccountStatus(
            account_id=account_config.id,
            balance=Decimal(account_info.balance).quantize(S.CENT, rounding=ROUND_HALF_UP),
            equity=Decimal(account_info.equity).quantize(S.CENT, rounding=ROUND_HALF_UP),
            profit=Decimal(account_info.profit).quantize(S.CENT, rounding=ROUND_HALF_UP)    ,
            trade_allowed=account_info.trade_allowed,
            trade_expert=account_info.trade_expert,
        )
        databaseService.saveAccountStatus(account_status)
        result = databaseService.getAccountMetatraderConnection(account_config.account_login, connected_mt5.id)
        if bool(result):
            new_account_metatrader_connection = AccountMetatraderConnection(
                account_config.id,
                connected_mt5.id
            )
            databaseService.addAccountMetatraderConnection(new_account_metatrader_connection)
        SingletonService().put(S.CONNECTED_ACCOUNT, account_config)
        return ["", symbols.callback.__name__.replace("_", "-")]

@click.command()
def create_account_with_password():
    global metatrader5Service
    account_info: None | AccountInfo

    connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if connected_mt5 is None:
        click.echo("No connected MT5 installation found. Please select the MT5 installation first.")
        mt5_installations: list[MetatraderConfig] = databaseService.listMetatraders()
        if len(mt5_installations) == 0:
            click.echo("No MT5 installations found.")
            return
        
        else:
            for index, mt5 in enumerate(mt5_installations, start=1):
                click.echo(f"{index}. {mt5}")

            choice = click.prompt("Enter the number of the MT5 installation to connect to", type=int)
            if 1 <= choice <= len(mt5_installations):
                mt5_to_connect: MetatraderConfig = mt5_installations[choice - 1]
                click.echo(empty_string)
                account_login = int(input("Login (account number): ").strip())
                password = getpass("Password: ")  # hidden while typing
                server = input("Server (e.g. MetaQuotes-Demo): ").strip()
                account_info: None | AccountInfo = metatrader5Service.login(account_login, password=password, server=server)    

    else:
        click.echo(empty_string)
        account_login = int(input("Login (account number): ").strip())
        password = getpass("Password: ")  # hidden while typing
        server = input("Server (e.g. MetaQuotes-Demo): ").strip()
        account_info: None | AccountInfo = metatrader5Service.login(account_login, password=password, server=server)
    
    if not bool(account_info):
        click.echo(f"Could not connect to metatrader with {account_login} - {'*' * len(password)} - {server}")
        return
    else:
        account_config: AccountConfig = databaseService.find_account_by_login_and_company(account_info.login, account_info.company)
        click.echo(f"{account_config}")
        if not bool(account_config):
            account_config = AccountConfig(
                currency=account_info.currency,
                company=account_info.company,
                leverage=account_info.leverage,
                account_login=account_info.login,
                name=account_info.name,
                password=password,
                server=account_info.server,
                trade_mode=account_info.trade_mode,
            )
            databaseService.saveAccountConfig(account_config)
        account_status: AccountStatus = databaseService.getAccountStatus(account_config.id)
        click.echo(f"{account_status}")
        if not bool(account_status):
            new_account_status = AccountStatus(
                account_id=account_config.id,
                balance=Decimal(account_info.balance).quantize(S.CENT, rounding=ROUND_HALF_UP),
                equity=Decimal(account_info.equity).quantize(S.CENT, rounding=ROUND_HALF_UP),
                profit=Decimal(account_info.profit).quantize(S.CENT, rounding=ROUND_HALF_UP)    ,
                trade_allowed=account_info.trade_allowed,
                trade_expert=account_info.trade_expert,
            )
            databaseService.saveAccountStatus(new_account_status)
        account_metatrader_connection: AccountMetatraderConnection = databaseService.getAccountMetatraderConnection(account_config.id, connected_mt5.id)
        click.echo(f"{account_metatrader_connection}")
        if not bool(account_metatrader_connection):
            account_metatrader_connection = AccountMetatraderConnection(
                account_config.id,
                connected_mt5.id
            )
            databaseService.addAccountMetatraderConnection(account_metatrader_connection)
        SingletonService().put(S.CONNECTED_ACCOUNT, account_config)
        click.echo(f"New account with login {account_config.account_login} and company {account_config.company} added to the database.")
        return ["", symbols.callback.__name__.replace("_", "-")]

@click.command()
def change_account_password():

    account_configs: list[AccountConfig] = databaseService.listAccountConfigs()
    if len(account_configs) == 0:
        click.echo("No Account Configs found.")
        return

    click.echo("Select an Account to connect to:")
    for index, mt5 in enumerate(account_configs, start=1):
        click.echo(f"{index}. {mt5}")

    choice = click.prompt("Enter the number of the Account to connect to", type=int)
    if 1 <= choice <= len(account_configs):
        account_to_change: AccountConfig = account_configs[choice - 1]
        password = getpass(f"New password for {account_to_change.account_login}: ")
        confirm = getpass("Confirm new password: ")
        if password == confirm:
            account_to_change.password = password
            databaseService.updateAccount(account_to_change)
            click.echo(f"Password for {account_to_change.account_login} updated")
        else:
            click.echo(f"Password for {account_to_change.account_login} did not match!")
    

@click.command()
def connect_account():
    """Connect account."""
    global metatrader5Service
    account_configs: list[AccountConfig] = databaseService.listAccountConfigs()
    if len(account_configs) == 0:
        click.echo("No Account Configs found.")
        return

    click.echo("Select an Account to connect to:")
    for index, mt5 in enumerate(account_configs, start=1):
        click.echo(f"{index}. {mt5}")

    choice = click.prompt("Enter the number of the Account to connect to", type=int)
    if 1 <= choice <= len(account_configs):
        account_to_connect: AccountConfig = account_configs[choice - 1]
        SingletonService().put(S.CONNECTED_ACCOUNT, account_to_connect)
        account_status: AccountStatus = databaseService.getAccountStatus(account_to_connect.id)
        account_info: AccountInfo = metatrader5Service.getAccountInfo()
        click.echo(f"{account_status}")
        if bool(account_status):
            account_status.balance=Decimal(account_info.balance).quantize(S.CENT, rounding=ROUND_HALF_UP)
            account_status.equity=Decimal(account_info.equity).quantize(S.CENT, rounding=ROUND_HALF_UP)
            account_status.profit=Decimal(account_info.profit).quantize(S.CENT, rounding=ROUND_HALF_UP)
            account_status.trade_allowed=account_info.trade_allowed
            account_status.account_idtrade_expert=account_info.trade_expert
            databaseService.updateAccountStatus(account_status)
        else: 
            click.echo(f"Could not update accountStatus")
        return ["", symbols.callback.__name__.replace("_", "-")]

ACCOUNT_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [no_accounts, explain_empty,  'List accounts', list_accounts.callback.__name__.replace("_", "-"), ], 
    [no_active_metatrader, explain_empty,  'Create account from MT5', create_account_mt5.callback.__name__.replace("_", "-"), ],  
    [no_accounts, explain_empty, 'Create account with Password etc...', create_account_with_password.callback.__name__.replace("_", "-"), ],
    [no_accounts, explain_empty, 'Change account Password', change_account_password.callback.__name__.replace("_", "-"), ], 
    [no_accounts, explain_empty, 'Connect account', connect_account.callback.__name__.replace("_", "-"), ], 
    [allow_allways, explain_empty,  'Return to previous menu', None, ]
]

@click.group()
@click.pass_context
def accounts(ctx: click.Context):
    """Status of Acounts"""
    global databaseService
    global metatrader5Service
    databaseService = SingletonService().get(S.DATABASE_SERVICE)
    metatrader5Service = SingletonService().get(S.METATRADER5_SERVICE)

    choice = None
    while True:
        """Show basic menu data"""
        account_configs: list[AccountConfig] = databaseService.listAccountConfigs()
        account_states: list[AccountStatus] = databaseService.listAccountStates()
        click.echo(empty_string)
        click.echo("Accounts:")
        if bool(account_configs) and len(account_configs) > 0:
            for account_config in account_configs:
                click.echo(f"- {account_config!r}")
                account_state = databaseService.getAccountStatus(account_config.id)
                if bool(account_state):
                    click.echo(f"\t - {account_state!r}")
        else:
            click.echo("No Account Configs found.")
        click.echo(empty_string)

        result = None
        if not bool(choice):
            choice = interactive_menu(ACCOUNT_SUB_COMMANDS, menuName="Settings - Accounts")
        
        if bool(choice):
            next_menu = ctx.invoke(ctx.command.commands[choice])
            # click.echo(f"Next_menu {Path(__file__).name}: {next_menu}")
            if bool(next_menu):
                return next_menu
            else: 
                choice = None  # Reset choice to None after invoking the command
        else:
            return result

accounts.add_command(list_accounts)
accounts.add_command(create_account_mt5)
accounts.add_command(create_account_with_password)
accounts.add_command(change_account_password)
accounts.add_command(connect_account)
