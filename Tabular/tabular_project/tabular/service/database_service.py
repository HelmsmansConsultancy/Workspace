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
from tabular.data.base.base import Base
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.orders.specific_pending_order import SpecificPendingOrder
from tabular.data.orders.specific_open_position import SpecificOpenPosition
from tabular_project.tabular.data.symbols.specific_symbol_info import SpecificSymbolInfomation
from tabular.data.orders.generic_pending_order import GenericPendingOrder
from tabular.data.orders.generic_open_position import GenericOpenPosition

class DatabaseService():
    db_file: str
    db_url: str
    engine: create_engine

    TOL = [5, 0.5, 0.05, 0.005, 0.0005, 0.00005, 0.000005, 0.000005]
    TOL3 = 0.005
    TOL4 = 0.0005
    TOL5 = 0.0005

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

########################################
#
#   SAVE
#
#########################################

    def saveAccountConfig(self, accountConfig: AccountConfig) -> int:
        with Session(self.engine) as session:
            session.add(accountConfig)
            session.commit()
            return accountConfig.id
    
    def saveAccountStatus(self, accountStatus: AccountStatus) -> int:
        with Session(self.engine) as session:
            session.add(accountStatus)
            session.commit()
            return accountStatus.account_id

    def saveSpecificSymbolInfomations(self, symbols: SpecificSymbolInfomation | list[SpecificSymbolInfomation]) -> None:
        with Session(self.engine) as session:
            if isinstance(symbols, list):
                for symbol in symbols:
                    session.add(symbol)
            else:
                session.add(symbols)
            session.commit()

    def saveSpecificOpenPositions(self, positions: list[SpecificOpenPosition]) -> None:
        with Session(self.engine) as session:
            for position in positions:
                session.add(position)
            session.commit()
    
    def saveGenericPendingOrder(self, genericOrder: GenericPendingOrder) -> int:
        with Session(self.engine) as session:
            session.add(genericOrder)
            session.commit()
            return genericOrder.id

########################################
#
#   UPDATE
#
#########################################

    def updateAccountConfig(self,  accountConfig: AccountConfig) -> None:
        with Session(self.engine) as session:
            session.merge(accountConfig)
            session.commit()

    def updateAccountStatus(self,  accountStatus: AccountStatus) -> None:
        with Session(self.engine) as session:
            session.merge(accountStatus)
            session.commit()

    def updateMetatraderConfig(self, metatraderConfig: MetatraderConfig) -> None:
        with Session(self.engine) as session:
            existing_metatrader = session.query(MetatraderConfig).filter(MetatraderConfig.id == metatraderConfig.id).first()
            if existing_metatrader:
                session.merge(metatraderConfig)
                session.commit()

    def updateSpecificSymbolInfomations(self, symbols: list[SpecificSymbolInfomation]) -> None:
        with Session(self.engine) as session:
            for symbol in symbols:
                session.merge(symbol)
            session.commit()

########################################
#
#   DELETE
#
#########################################
        
    def deleteSpecificPendingOrder(self, order: SpecificPendingOrder) -> None:
        with Session(self.engine) as session:
            session.delete(order)


    def removeOpenPositions(self, openPositions: list[SpecificOpenPosition]) -> None:
        with Session(self.engine) as session:
            for position in openPositions:
                session.delete(position)
            session.commit()



########################################
#
#   COUNT
#
#########################################
        
    def countGenericOrders(self) -> int:
        with Session(self.engine) as session:
            count = session.query(GenericPendingOrder).count()
            return count

    def countGenericPendingOrders(self) -> int:
        with Session(self.engine) as session:
            count = session.query(GenericPendingOrder).count()
            return count

    def countRowsInTable(self, tableName: str) -> int:
        with  Session(self.engine) as session:
            count: int = session.execute(text(f'SELECT COUNT(*) FROM "{tableName}"')).scalar()
            return count

    def countMetatraderConfigs(self) -> int:
        with Session(self.engine) as session:
            count = session.query(MetatraderConfig).count()
            return count

    def countAccounts(self) -> int:
        with Session(self.engine) as session:
            count = session.query(AccountConfig).count()
            return count
        
    def countGenericOpenPositions(self) -> int:
        with Session(self.engine) as session:
            count = session.query(GenericOpenPosition).count()
            return count
       

########################################
#
#   COUNT BY ACCOUNT
#
#########################################
    
    def countSpecificOpenPositions(self, accountId) -> int:
        with Session(self.engine) as session:
            count = session.query(SpecificOpenPosition).filter(SpecificOpenPosition.account_id == accountId).count()
            return count
        
    def countSpecificPendingOrders(self, accountId) -> int:
        with Session(self.engine) as session:
            count = session.query(SpecificPendingOrder).filter(SpecificPendingOrder.account_id == accountId).count()
            return count
        
    def countSymbolInformation(self, accountId: int) -> int:
        with Session(self.engine) as session:
            count = session.query(SpecificSymbolInfomation).filter(SpecificSymbolInfomation.account_id == accountId).count()
            return count
    
########################################
#
#   LIST
#
#########################################

    def listTablesInDatabase(self) -> list[str]:
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        return tables

    def listAccountConfigs(self) -> list[AccountConfig]:
        with Session(self.engine) as session:
            account_configs = session.query(AccountConfig).all()
            return account_configs

    def listAccountStates(self) -> list[AccountStatus]:
        with Session(self.engine) as session:
            account_states = session.query(AccountStatus).all()
            return account_states

    def listMetatraders(self) -> list[MetatraderConfig]:
        with Session(self.engine) as session:
            metatraders = session.query(MetatraderConfig).all()
            return metatraders


########################################
#
#   SPECIAL
#
#########################################


    def getGenericOrderByStats(self, digits: int, entry: float, sl: float, tp: float) -> GenericPendingOrder:
        self.console.print(f"Searching entry {entry - self.TOL[digits]} - {entry + self.TOL[digits]}, sl {sl - self.TOL[digits]} - {entry + self.TOL[digits]}, tp {tp - self.TOL[digits]} - {tp + self.TOL[digits]}")
        with Session(self.engine) as session:
            found = session.query(GenericPendingOrder).filter(
                GenericPendingOrder.digits == digits,
                GenericPendingOrder.entry.between(entry - self.TOL[digits], entry + self.TOL[digits]),
                GenericPendingOrder.sl.between(sl - self.TOL[digits], sl + self.TOL[digits]),
                GenericPendingOrder.tp.between(tp - self.TOL[digits], tp + self.TOL[digits]),
            ).first()
            self.console.print(f"Found in DB: {found}")
            return found

     
    def getAccountStatus(self, account_id: int) -> AccountStatus:
        with Session(self.engine) as session:
            account_state = session.query(AccountStatus).filter(AccountStatus.account_id == account_id).first()
            return account_state
    

    def find_account_by_login_and_company(self, accountLogin: int, company: str) -> AccountConfig | None:
        with Session(self.engine) as session:
            account_config = session.query(AccountConfig).filter(AccountConfig.account_login==accountLogin, AccountConfig.company==company).first()
            return account_config

    def getAccount(self, account_id: int) -> AccountConfig | None:
        with Session(self.engine) as session:
            account_config = session.get(AccountConfig, account_id)
            return account_config
        
        
    def addAccountMetatraderConnection(self, accountMetatraderConnection: AccountMetatraderConnection):
        with Session(self.engine) as session:
            session.add(accountMetatraderConnection)
            session.commit()

    def getAccountMetatraderConnection(self, accountId: int, metatraderId: int) -> AccountMetatraderConnection:
        with Session(self.engine) as session:
            connection: AccountMetatraderConnection = session.query(AccountMetatraderConnection).filter(AccountMetatraderConnection.account_id==accountId, AccountMetatraderConnection.metatrader_id==metatraderId).first()
            return connection

    def list_account_metatrader_connections_by_account(self, accountId: int) -> list[AccountMetatraderConnection]:
        with Session(self.engine) as session:
            accountMetatraderConnections: AccountMetatraderConnection = session.query(AccountMetatraderConnection).filter(AccountMetatraderConnection.account_id==accountId).all()
            return accountMetatraderConnections

    def list_account_metatrader_connections_by_metatrader(self, metatrader_id: int) -> list[AccountMetatraderConnection]:
        with Session(self.engine) as session:
            accountMetatraderConnections: AccountMetatraderConnection = session.query(AccountMetatraderConnection).filter(AccountMetatraderConnection.metatrader_id==metatrader_id).all()
            return accountMetatraderConnections

    def addMetatrader(self, metatraderConfig: MetatraderConfig) -> MetatraderConfig:
        with Session(self.engine) as session:
            session.add(metatraderConfig)
            session.commit()
            session.refresh(metatraderConfig)
            return metatraderConfig
        
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

    def getPendingOrders(self, accountId) -> list[SpecificPendingOrder]:
        with Session(self.engine) as session:  
            pendingOrders = session.query(SpecificPendingOrder).filter(SpecificPendingOrder.account_id == accountId).all()
            return pendingOrders

    def updatePendingOrders(self, pendingOrders: list[SpecificPendingOrder] ) -> None:
        with Session(self.engine) as session:
            for order in pendingOrders:
                # self.console.print(f"updating: {order}")
                session.merge(order)
            session.commit()
    
    def addPendingOrders(self, pendingOrders: list[SpecificPendingOrder]) -> None:
        with Session(self.engine) as session:
            for order in pendingOrders:
                # self.console.print(f"adding: {order!r}")
                session.add(order)
            session.commit()

    def removePendingOrders(self, pendingOrders: list[SpecificPendingOrder]) -> None:
        with Session(self.engine) as session:
            for order in pendingOrders:
                session.delete(order)
            session.commit()
        

          
    def getTradeDeals(self, accountId) -> list[SpecificOpenPosition]:
        with Session(self.engine) as session:  
            openPositions = session.query(SpecificOpenPosition).filter(SpecificOpenPosition.account_id == accountId).all()
            return openPositions

    def updateOpenPositions(self, openPositions: list[SpecificOpenPosition] ) -> None:
        with Session(self.engine) as session:
            for position in openPositions:
                # self.console.print(f"updating: {position}")
                session.merge(position)
            session.commit()
    

    def getSymbolInformation(self, accountId: int) -> list[SpecificSymbolInfomation]:
        with Session(self.engine) as session:
            symbolInfomations = session.query(SpecificSymbolInfomation).filter(SpecificSymbolInfomation.account_id == accountId).all()
            return symbolInfomations
        
    def getGenericOrders(self) -> list[GenericPendingOrder]:
        with Session(self.engine) as session:
            genericOrders = session.query(GenericPendingOrder).all()
            return genericOrders

    def saveGenericPendingOrder(self, genericOrder: GenericPendingOrder) -> int:
        with Session(self.engine) as session:
            session.add(genericOrder)
            session.commit()
            return genericOrder.id

    def getSymbolInformationBySymbol(self, accountId: int, symbol: str) -> SpecificSymbolInfomation:
        with Session(self.engine) as session:
            symbol: SpecificSymbolInfomation = session.query(SpecificSymbolInfomation).filter(SpecificSymbolInfomation.account_id == accountId, SpecificSymbolInfomation.symbol == symbol).first()
            return symbol


    def getGenericPendingOrders(self) -> list[GenericPendingOrder]:
        with Session(self.engine) as session:
            orders = session.query(GenericPendingOrder).all()
            return orders


    