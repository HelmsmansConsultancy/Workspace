from rich.console import Console 
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.settings.account_config import AccountConfig
from tabular.service.singleton_service import SingletonService
from tabular.service.s import S
from tabular.service.database_service import DatabaseService


console = Console()

empty_string = ""

def allow_allways():
    return True

def no_metatraders():
    databaseService: DatabaseService =  SingletonService().get(S.DATABASE_SERVICE)
    metatraders = databaseService.countMetatraders()
    if metatraders > 0:
        return True
    else:
        return False

def no_active_metatrader():
    connected_metatrader: AccountConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if bool(connected_metatrader):
        return True
    else:
        return False 

def no_accounts():
    databaseService: DatabaseService =  SingletonService().get(S.DATABASE_SERVICE)
    accounts = databaseService.countAccounts()
    if accounts > 0:
        return True
    else:
        return False

def no_active_account():
    connected_account: AccountConfig | None = SingletonService().get(S.CONNECTED_ACCOUNT)
    if bool(connected_account):
        return True
    else:
        return False 

def allow_never():
    return False
