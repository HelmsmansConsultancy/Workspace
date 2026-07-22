import click
# from pathlib import Path
from rich.console import Console
from typing import Callable
from MetaTrader5 import SymbolInfo
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.service.s import S
from tabular.util.menu.menus_allow import empty_string, allow_allways, no_active_account, no_accounts
from tabular.util.menu.menus_explain import explain_accounts, explain_DB, explain_generic_pending_orders, explain_specific_open_positions, explain_symbols, explain_empty
from tabular.util.menu.menus_utils import interactive_menu
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.settings.account_config import AccountConfig
from tabular_project.tabular.data.symbols.specific_symbol_info import SpecificSymbolInfomation
from tabular.util.util.symbols_util import copyValuesInto
from tabular.commands.orders_account.menu_account_orders import menu_account_orders

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
    symbolInfos: list[SymbolInfo] = metatrader5Service.getSymbolInfo(connect_account.id)
    symbolInformations: list[SpecificSymbolInfomation] = databaseService.getSymbolInformation(connect_account.id)
    newSymbols: list[SpecificSymbolInfomation] = []
    existingSymbols: list[SpecificSymbolInfomation] = []
    for symbolInfo in symbolInfos:
        existingSymbol = next((symbol for symbol in symbolInformations if symbol.name == symbolInfo.name), None)
        if bool(existingSymbol): 
            copyValuesInto(symbolInfo, existingSymbol)
            click.echo(f"Existing: {existingSymbol}")
            existingSymbols.append(existingSymbol)
        else:
            newSymbol =SpecificSymbolInfomation(
                account_id=connect_account.id,      
            )
            copyValuesInto(symbolInfo, newSymbol)
            click.echo(f"New: {newSymbol}")
            newSymbols.append(newSymbol)
    databaseService.saveSpecificSymbolInfomations(newSymbols)
    databaseService.updateSpecificSymbolInfomations(existingSymbols)
    return ["", menu_account_orders.callback.__name__.replace("_", "-")]


@click.command()
def list_symbolinfo():
    """The list of symbols"""
    connected_account: AccountConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    click.echo(empty_string)
    if bool(connected_account):
        symbols = databaseService.getSymbolInformation(connected_account.id)
        if len(symbols) > 0:
            for symbol in symbols:
                click.echo(f"{symbol}") 
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
    
    choice = None
    while True:
        """Show basic menu data"""    
        click.echo(empty_string)
        if bool(connected_account):
            symbols = databaseService.countSymbolInformation(connected_account.id)
            if symbols > 0:
                click.echo(f"<{symbols} Symbol(s) in Account  {connected_account.name}>") 
            else:
                click.echo(f"<No Symbol(s)  in Account  {connected_account.name}>")
        else:
            click.echo(f"<No Account connected>")

        if choice is None:
            choice = interactive_menu(SYMBOLS_SUB_COMMANDS, menuName="Symbols")

        result = None
        if bool(choice):
            next_menu: list[str] = ctx.invoke(ctx.command.commands[choice])
            # click.echo(f"Next_menu {Path(__file__).name}: {next_menu}")
            if bool(next_menu):
                if len(next_menu) > 1:
                    return next_menu[1:]
                else:
                    choice = next_menu[0]
            else:
                choice = None  # Reset choice to None after invoking the command
        else:
            return
        
symbols.add_command(get_symbolinfo)
symbols.add_command(list_symbolinfo)

