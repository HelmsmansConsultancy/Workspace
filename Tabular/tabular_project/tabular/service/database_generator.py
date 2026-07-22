import os
from rich.console import Console
from sqlalchemy import create_engine
from tabular.data.base import Base
from tabular.data.settings.account_config import AccountConfig
from tabular.data.settings.account_status import AccountStatus
from tabular.data.settings.account_metatrader_connection import AccountMetatraderConnection
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.symbols.specific_symbol_info import SpecificSymbolInfomation
from tabular.data.symbols.generic_symbol_info import GenericSymbolInfomation
from tabular.data.orders.specific_pending_order import SpecificPendingOrder
from tabular.data.orders.specific_open_position import SpecificOpenPosition
from tabular.data.orders.generic_pending_order import GenericPendingOrder
from tabular.data.orders.generic_open_position import GenericOpenPosition
from rich.traceback import install
import traceback, sys


install(show_locals=True) 

class DatabaseGenerator():
    db_file: str
    db_url: str

    def generateEngine(self):
        self.console = Console()
        self.db_file = os.getcwd()  + ".db"
        self.db_url = f"sqlite:///{self.db_file}"
        self.console.print(f"Starting database at: {self.db_file}")
        self.engine = create_engine(self.db_url, echo=True, future=True)
        for name, table in Base.metadata.tables.items():
            print(name)
        try:
            Base.metadata.create_all(
                self.engine,
                tables=[
                    AccountConfig,
                    AccountStatus,
                    AccountMetatraderConnection,
                    MetatraderConfig,
                    GenericSymbolInfomation,
                    SpecificSymbolInfomation,
                    SpecificPendingOrder,
                    SpecificOpenPosition,
                    GenericPendingOrder,
                    GenericOpenPosition,
            ])
        except TypeError:
            tb = sys.exc_info()[2]
            # walk to the last frame and dump its locals
            while tb.tb_next:
                tb = tb.tb_next
            print("Locals at failure point:")
            for k, v in tb.tb_frame.f_locals.items():
                print(f"  {k!r} = {v!r}  ({type(v).__name__})")
            raise
        return self.engine
        