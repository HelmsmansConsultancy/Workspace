import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session
from rich.console import Console
from tabular.service.s import S
from tabular.data.settings.account_config import AccountConfig
from tabular.data.settings.account_status import AccountStatus
from tabular.data.settings.account_metatrader_connection import AccountMetatraderConnection
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.service.singleton_service import SingletonService
from tabular.data.base import Base
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.application_config import ApplicationConfig
from tabular.data.pending_order import PendingOrder
from tabular.data.open_position import OpenPosition
from tabular.data.symbols.symbol_info import SymbolInfomation
from tabular.data.generic_order import GenericOrder
from tabular.data.generic_position import GenericPosition

applicationConfig: ApplicationConfig = None

class DatabaseService():
    db_file: str
    db_url: str
    engine: create_engine

    TOL = 0.0005

    def __init__(self):
        global applicationConfig
        self.console = Console()
        applicationConfig = SingletonService().get(S.APPLICATION_CONFIG)
        if bool(applicationConfig):
            self.db_file = applicationConfig.db_file
        else:
            self.db_file = os.getcwd()  + ".db"
            self.console.print("No ApplicationConfig !!!")
        self.db_url = f"sqlite:///{self.db_file}"
        self.console.print(f"Starting database at: {self.db_file}")
        self.engine = create_engine(self.db_url, echo=False, future=True)
        Base.metadata.create_all(self.engine)

    def listTables(self) -> list[str]:
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        return tables
    
    def countRows(self, tableName: str) -> int:
        with  Session(self.engine) as session:
            count: int = session.execute(text(f'SELECT COUNT(*) FROM "{tableName}"')).scalar()
            return count

    def list_account_configs(self) -> list[AccountConfig]:
        with Session(self.engine) as session:
            account_configs = session.query(AccountConfig).all()
            return account_configs
    
    def list_account_states(self) -> list[AccountStatus]:
        with Session(self.engine) as session:
            account_states = session.query(AccountStatus).all()
            return account_states
    
    def countAccounts(self) -> int:
        with Session(self.engine) as session:
            count = session.query(AccountConfig).count()
            return count

    def find_account_by_login_and_company(self, login: int, company: str) -> AccountConfig | None:
        with Session(self.engine) as session:
            account_config = session.query(AccountConfig).filter_by(login=login, company=company).first()
            return account_config

    def getAccount(self, account_id: int) -> AccountConfig | None:
        with Session(self.engine) as session:
            account_config = session.get(AccountConfig, account_id)
            return account_config

    def addAccount(self, accountConfig: AccountConfig) -> int:
        with Session(self.engine) as session:
            session.add(accountConfig)
            session.commit()
            return accountConfig.id
        
    def addAccountStatus(self, accountStatus: AccountStatus) -> int:
        with Session(self.engine) as session:
            session.add(accountStatus)
            session.commit()
            return accountStatus.account_id
        
    def addAccountMetatraderConnection(self, accountMetatraderConnection: AccountMetatraderConnection):
        with Session(self.engine) as session:
            session.add(accountMetatraderConnection)
            session.commit()

    def list_account_metatrader_connections_by_account(self, accountId: int) -> list[AccountMetatraderConnection]:
        with Session(self.engine) as session:
            accountMetatraderConnections: AccountMetatraderConnection = session.query(AccountMetatraderConnection).filter_by(account_id= accountId).all()
            return accountMetatraderConnections

    def list_account_metatrader_connections_by_metatrader(self, metatrader_id: int) -> list[AccountMetatraderConnection]:
        with Session(self.engine) as session:
            accountMetatraderConnections: AccountMetatraderConnection = session.query(AccountMetatraderConnection).filter(AccountMetatraderConnection.metatrader_id==metatrader_id).all()
            return accountMetatraderConnections

    def listMetatraders(self) -> list[MetatraderConfig]:
        with Session(self.engine) as session:
            metatraders = session.query(MetatraderConfig).all()
            return metatraders

    def countMetatraders(self) -> int:
        with Session(self.engine) as session:
            count = session.query(MetatraderConfig).count()
            return count

    def addMetatrader(self, metatraderConfig: MetatraderConfig) -> MetatraderConfig:
        with Session(self.engine) as session:
            session.add(metatraderConfig)
            session.commit()
            session.refresh(metatraderConfig)
            return metatraderConfig
        
    def updateMetatrader(self, metatraderConfig: MetatraderConfig) -> None:
        with Session(self.engine) as session:
            existing_metatrader = session.query(MetatraderConfig).filter(MetatraderConfig.id == metatraderConfig.id).first()
            if existing_metatrader:
                session.merge(metatraderConfig)
                session.commit()

    def getMetatradersByPath(self, metatraderPath: str) -> list[MetatraderConfig]:
        with Session(self.engine) as session:
            metatraders = session.query(MetatraderConfig).filter(MetatraderConfig.path == metatraderPath).all()
            return metatraders
    
    def deleteMetatrader(self, metatraderId: int) -> None:
        with Session(self.engine) as session:
            metatrader = session.query(MetatraderConfig).filter(MetatraderConfig.id == metatraderId).first()
            if bool(metatrader):
                session.delete(metatrader)
                session.commit()

    def accounts(self) -> list[AccountConfig]:
        with Session(self.engine) as session:
            accounts = session.query(AccountConfig).all()
            return accounts
        
    def countGenericOrders(self) -> int:
        with Session(self.engine) as session:
            count = session.query(GenericOrder).count()
            return count

    
    def countPendingOrders(self, accountId) -> int:
        with Session(self.engine) as session:
            count = session.query(PendingOrder).filter(PendingOrder.account_id == accountId).count()
            return count
        
    def getPendingOrders(self, accountId) -> list[PendingOrder]:
        with Session(self.engine) as session:  
            pendingOrders = session.query(PendingOrder).filter(PendingOrder.account_id == accountId).all()
            return pendingOrders

    def updatePendingOrders(self, pendingOrders: list[PendingOrder] ) -> None:
        with Session(self.engine) as session:
            for order in pendingOrders:
                # self.console.print(f"updating: {order}")
                session.merge(order)
            session.commit()
    
    def addPendingOrders(self, pendingOrders: list[PendingOrder]) -> None:
        with Session(self.engine) as session:
            for order in pendingOrders:
                # self.console.print(f"adding: {order!r}")
                session.add(order)
            session.commit()

    def removePendingOrders(self, pendingOrders: list[PendingOrder]) -> None:
        with Session(self.engine) as session:
            for order in pendingOrders:
                # self.console.print(f"deleting: {order}")
                session.delete(order)
            session.commit()
            
    def countOpenPositions(self, accountId) -> int:
        with Session(self.engine) as session:
            count = session.query(OpenPosition).filter(OpenPosition.account_id == accountId).count()
            return count
        
    def countGenericPositions(self) -> int:
        with Session(self.engine) as session:
            count = session.query(GenericPosition).count()
            return count

          
    def getTradeDeals(self, accountId) -> list[OpenPosition]:
        with Session(self.engine) as session:  
            openPositions = session.query(OpenPosition).filter(OpenPosition.account_id == accountId).all()
            return openPositions

    def updateOpenPositions(self, openPositions: list[OpenPosition] ) -> None:
        with Session(self.engine) as session:
            for position in openPositions:
                # self.console.print(f"updating: {position}")
                session.merge(position)
            session.commit()
    
    def addOpenPositions(self, openPositions: list[OpenPosition]) -> None:
        with Session(self.engine) as session:
            for position in openPositions:
                # self.console.print(f"adding: {position!r}")
                session.add(position)
            session.commit()

    def removeOpenPositions(self, openPositions: list[OpenPosition]) -> None:
        with Session(self.engine) as session:
            for position in openPositions:
                # self.console.print(f"deleting: {position}")
                session.delete(position)
            session.commit()

    def getSymbolInformation(self, accountId: int) -> list[SymbolInfomation]:
        with Session(self.engine) as session:
            symbolInfomations = session.query(SymbolInfomation).filter(SymbolInfomation.account_id == accountId).all()
            return symbolInfomations
        
    def getGenericOrders(self) -> list[GenericOrder]:
        with Session(self.engine) as session:
            genericOrders = session.query(GenericOrder).all()
            return genericOrders

    def getGenericOrderByStats(self, entry: float, sl: float, tp: float) -> GenericOrder:
        with Session(self.engine) as session:
            session.query(GenericOrder).filter(
                GenericOrder.entry.between(entry - self.TOL, entry + self.TOL),
                GenericOrder.sl.between(sl - self.TOL, sl + self.TOL),
                GenericOrder.tp.between(tp - self.TOL, tp + self.TOL),
            ).first()

    def addGenericOrder(self, genericOrder: GenericOrder) -> int:
        with Session(self.engine) as session:
            session.add(genericOrder)
            session.commit()
            return genericOrder.id

    def getSymbolInformationBySymbol(self, symbol: str):
        with Session(self.engine) as session:
            symbol: SymbolInfomation = session.query(SymbolInfomation).filter(SymbolInfomation.pair == symbol).first()
            return symbol

    def countSymbolInformation(self, accountId: int) -> int:
        with Session(self.engine) as session:
            count = session.query(SymbolInfomation).filter(SymbolInfomation.account_id == accountId).count()
            return count

    def addSymbolInfo(self, symbols: list[SymbolInfomation]) -> None:
        with Session(self.engine) as session:
            for symbol in symbols:
                # self.console.print(f"adding: {symbol!r}")
                session.add(symbol)
            session.commit()
    
    def updateSymbolInformation(self, existingSymbols: list[SymbolInfomation]) -> None:
        with Session(self.engine) as session:
            for symbol in existingSymbols:
                # self.console.print(f"adding: {symbol!r}")
                session.merge(symbol)
            session.commit()



    