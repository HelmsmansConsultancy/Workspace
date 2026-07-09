from rich.console import Console
from tabular.service.s import S
from tabular.util.menuutils import interactive_menu, empty_string
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.service.metatrader_5_service import Metatrader5Service
from tabular.data.metatrader_config import MetatraderConfig
from tabular.data.application_config import ApplicationConfig


class MenuService():
    console: Console
    applicationConfig: ApplicationConfig
    databaseService: DatabaseService
    metatrader5Service: Metatrader5Service

    def __init__(self):
        self.console = Console()
        self.applicationConfig: ApplicationConfig = None
        self.databaseService: DatabaseService = None
        self.metatrader5Service: Metatrader5Service = None
