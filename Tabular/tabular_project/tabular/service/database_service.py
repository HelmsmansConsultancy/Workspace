from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from typing import cast
from rich.console import Console
from tabular.service.s import S
from tabular.data.account_config import AccountConfig
from tabular.data.metatrader_config import MetatraderConfig
from tabular.service.singleton_service import SingletonService
from tabular.data.base import Base
from tabular.data.metatrader_config import MetatraderConfig
from tabular.data.application_config import ApplicationConfig

console = Console()

class DatabaseService():
    db_file: str
    db_url: str
    engine: create_engine

    def __init__(self):
        self.console = Console()
        self.db_file = cast(AccountConfig, SingletonService().get(S.APPLICATION_CONFIG)).db_file
        self.db_url = f"sqlite:///{self.db_file}"
        self.console.print(f"Starting database at: {self.db_file}")
        self.engine = create_engine(self.db_url, echo=False, future=True)
        Base.metadata.create_all(self.engine)

    def listTables(self) -> list[str]:
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        return tables

    def list_account_configs(self) -> list[AccountConfig]:
        with Session(self.engine) as session:
            account_configs = session.query(AccountConfig).all()
            return account_configs
    
    def countAccounts(self) -> int:
        with Session(self.engine) as session:
            count = session.query(AccountConfig).count()
            return count

    def find_account_by_login_and_company(self, login: int, company: str) -> AccountConfig | None:
        with Session(self.engine) as session:
            account_config = session.query(AccountConfig).filter_by(login=login, company=company).first()
            return account_config

    def addAccount(self, accountConfig: AccountConfig) -> int:
        with Session(self.engine) as session:
            session.add(accountConfig)
            session.commit()
            return accountConfig.id

    def listMetatraders(self) -> list[MetatraderConfig]:
        with Session(self.engine) as session:
            metatraders = session.query(MetatraderConfig).all()
            return metatraders

    def countMetatraders(self) -> int:
        with Session(self.engine) as session:
            count = session.query(MetatraderConfig).count()
            return count

    def addMetatrader(self, metatraderConfig: MetatraderConfig) -> int:
        with Session(self.engine) as session:
            session.add(metatraderConfig)
            session.commit()
            return metatraderConfig.id
        
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
    

    