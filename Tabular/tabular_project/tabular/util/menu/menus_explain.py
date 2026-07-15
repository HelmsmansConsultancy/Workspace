from rich.console import Console 
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.settings.account_config import AccountConfig
from tabular.service.singleton_service import SingletonService
from tabular.service.s import S
from tabular.service.database_service import DatabaseService


console = Console()

empty_string = ""

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

def explain_DB(enabled:bool = True):
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    message: None
    if databaseService is not None:
        message = f"\t\t\t<{databaseService.db_file}>"
    else:
        message = "\t\t\t<No database available.>"
    if not enabled:
        message += " (Disabled)"
    return message

def explain_empty(enabled:bool = True):
    return empty_string

def explain_generic_orders(enabled = True):
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)

    generic_orders = databaseService.countGenericOrders()
    generic_positions = databaseService.countGenericPositions()
    
    message = ""
    if generic_orders > 0:
        message += f"\t\t<{generic_orders} generic order(s)>"
    else:
        message += f"\t\t<No pending orders>"

    if generic_positions > 0:
        message += f"\t\t<{generic_positions} generic position(s)>"
    else:
        message += f"\t\t<No open positions>"

    return message

def explain_account_orders(enabled = True):
    connected_account: AccountConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    message = ""
    if bool(connected_account):
        pending_orders = databaseService.countPendingOrders(connected_account.id)
        open_positions = databaseService.countOpenPositions(connected_account.id)
        if pending_orders > 0:
            message += f"\t\t<{pending_orders} pending order(s)>"
        else:
            message += f"\t\t<No pending orders>"
        
        if open_positions > 0:
            message += f"\t\t<{open_positions} open position(s)>"
        else:
            message += f"\t\t<No open positions>"
    else:
        message += f"\t\t<No database available.>"
    return message

def explain_pending_orders(enabled:bool = True):
    connected_account: AccountConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    if bool(connected_account):
        pending_orders = databaseService.countPendingOrders(connected_account.id)
        if pending_orders > 0:
            message = f"\t\t<{pending_orders} pending order(s)>"
        else:
            message = f"\t\t<No pending orders>"
    else:
        message = f"\t\t<No database available.>"
    return message

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


def explain_settings(enabled:bool = True):
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    message: None
    if databaseService is not None:
        message = f"\t\t\t<{databaseService.db_file}>"
    else:
        message = "\t\t\t<No database available.>"
    if not enabled:
        message += " (Disabled)"
    
    if databaseService is not None:
        mt5_installations = databaseService.countMetatraders()
        if mt5_installations > 0:
            message += f" <{mt5_installations} MT5 installation(s)>"
        else:
            message += " <No MT5 installations found.>"
    else:
        message += " <No database available.>"

    connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if bool(connected_mt5):
        message += f" <Connected to: {connected_mt5.name}>"
    else:
        message += " <Not connected>"
    
    if not enabled:
        message += " (Disabled)"

    if databaseService is not None:
        accounts = databaseService.countAccounts()
        if accounts > 0:
            message += f" <{accounts} account(s)>"
        else:
            message += " <No accounts>"
    else:
        message += "<No database available.>"

    connected_account: MetatraderConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    if bool(connected_account):
        message += f" <Connected with: {connected_account.name}>"
    else:
        message += " <Not connected>"
    
    if not enabled:
        message += " (Disabled)"
    return message

def explain_symbols(enabled:bool = True):
    connected_account: AccountConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    if bool(connected_account):
        symbols = databaseService.countSymbolInformation(connected_account.id)
        if symbols > 0:
            message = f"\t\t\t<{symbols} Symbol(s)>"
        else:
            message = f"\t\t\t<No Symbols>"
    else:
        message = f"\t\t\t<No database available.>"
    return message

def explain_open_positions(enabled:bool = True):
    connected_account: AccountConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    databaseService: DatabaseService = SingletonService().get(S.DATABASE_SERVICE)
    if bool(connected_account):
        openPositions = databaseService.countOpenPositions(connected_account.id)
        if openPositions > 0:
            message = f"\t\t<{openPositions} open position(s)>"
        else:
            message = f"\t\t<No open positions>"
    else:
        message = f"\t\t<No database available.>"
    return message