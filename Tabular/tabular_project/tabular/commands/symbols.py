import click
from rich.console import Console
from typing import Callable
from MetaTrader5 import AccountInfo, SymbolInfo
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.service.s import S
from tabular.util.menus_allow import empty_string, allow_allways, no_active_account, no_accounts
from tabular.util.menus_explain import explain_accounts, explain_DB, explain_pending_orders, explain_open_positions, explain_symbols, explain_empty
from tabular.util.menus_utils import interactive_menu
from tabular.data.metatrader_config import MetatraderConfig
from tabular.data.account_config import AccountConfig
from tabular.data.symbol_info import SymbolInfomation
from tabular.util.symbols_util import copyValuesInto
from tabular.data.application_config import ApplicationConfig

console = Console()
databaseService: DatabaseService = None
metatrader5Service: Metatrader5Service = None


@click.command()
def get_symbolinfo():
    """ Get all the symbol info"""
    global metatrader5Service
    global databaseService

    connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if connected_mt5 is None:
        click.echo("No connected MT5 installation found. Please connect to an MT5 installation first.")
        return
    
    connect_account = SingletonService().get(S.CONNECTED_ACCOUNT)
    symbolInfos: list[SymbolInfo] = metatrader5Service.getSymbolInfo(connected_mt5.id)
    symbols: list[SymbolInfomation] = databaseService.getSymbolInformation(connected_mt5.id)
    newSymbols: list[SymbolInfomation] = []
    existingSymbols: list[SymbolInfomation] = []
    for symbolInfo in symbolInfos:
        click.echo(symbolInfo.name)
        existingSymbol = next((symbol for symbol in symbols if symbol.name == symbolInfo.name), None)
        if bool(existingSymbol): 
            copyValuesInto(symbolInfo, existingSymbol)
            click.echo(f"Existing: {existingSymbol}")
            existingSymbols.append(existingSymbol)
        else:
            newSymbol =SymbolInfomation(
                account_id=connect_account.id,      
            )
            copyValuesInto(symbolInfo, newSymbol)
            click.echo(f"New: {newSymbol}")
            newSymbols.append(newSymbol)
    databaseService.addSymbolInfo(newSymbols)
    databaseService.updateSymbolInformation(existingSymbols)


@click.command()
def list_symbolinfo():
    """The list of symbols"""
    connected_account: AccountConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    click.echo(empty_string)
    if bool(connected_account):
        symbols = databaseService.getSymbolInformation(connected_account.id)
        if len(symbols) > 0:
            for symbol in symbols:
                click.echo(f"<{symbols}>") 
        else:
            click.echo(f"<No Symbol(s)  in Account  {connected_account.name}>")
    else:
        click.echo(f"<No Account connected>")
    click.echo(empty_string)


SYMBOLS_SUB_COMMANDS: list[tuple[Callable[[], bool],  Callable[[bool], str], str, str | None,]] = [
    [no_accounts, explain_empty, 'Get Symbol Info', get_symbolinfo.callback.__name__.replace("_", "-"),],
    [no_accounts, explain_empty, 'List Symbol Info', list_symbolinfo.callback.__name__.replace("_", "-"),],
    [allow_allways, explain_empty, 'Return to previous menu', None, ]
]


@click.group()
@click.pass_context
def symbols(ctx: click.Context):
    """Status of symbols."""
    global metatrader5Service
    global databaseService

    connected_account: AccountConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    metatrader5Service = SingletonService().get(S.METATRADER5_SERVICE)
    databaseService = SingletonService().get(S.DATABASE_SERVICE)
    
    if bool(connected_account):
        symbols = databaseService.countSymbolInformation(connected_account.id)
        if symbols > 0:
            click.echo(f"<{symbols} Symbol(s) in Account  {connected_account.name}>") 
        else:
            click.echo(f"<No Symbol(s)  in Account  {connected_account.name}>")
    else:
        click.echo(f"<No Account connected>")
    
    choice = None
    while True:
        if choice is None:
            choice = interactive_menu(SYMBOLS_SUB_COMMANDS)

        result = None
        if bool(choice):
            ctx.invoke(ctx.command.commands[choice])
            choice = None  # Reset choice to None after invoking the command
        else:
            return result
        
symbols.add_command(get_symbolinfo)
symbols.add_command(list_symbolinfo)

