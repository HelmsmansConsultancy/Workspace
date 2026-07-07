import sqlite3
from sqlite3 import Connection
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import cast
from rich.console import Console
from tabular.data.account_config import AccountConfig
from tabular.data.metatrader_config import MetatraderConfig
from tabular.service.singleton_service import SingletonService
from tabular.data.base import Base
from tabular.data.metatrader_config import MetatraderConfig
from tabular.data.application_config import ApplicationConfig

console = Console()

class DatabaseService():
    db_file: str
    connection: Connection

    def __init__(self):
        self.console = Console()
        self.db_file = cast(AccountConfig, SingletonService().get("ApplicationConfig")).db_file
        self.console.print(f"Starting database at: {self.db_file}")
        self.engine =  create_engine(self.db_fil, echo=True)
        Base.metadata.create_all(self.engine)
        #self.connection = sqlite3.connect(self.db_file)

        #cursor = self.connection
        #cursor.execute("""
        #    CREATE TABLE IF NOT EXISTS METATRADER_CONFIG (id INTEGER PRIMARY KEY, 
        #                   path TEXT NOT NULL)
        #""")

        #cursor.execute("""
        #    CREATE TABLE IF NOT EXISTS ACCOUNT_CONFIG (id INTEGER PRIMARY KEY, 
        #                   account_id TEXT NOT NULL,
        #                   metatrader_id INTEGER NOT NULL,
        #                   FOREIGN KEY(metatrader_id) REFERENCES METATRADER_CONFIG(id))
        #""")

    def listTables(self) -> list[str]:
        with Session(self.engine) as session:
            tables = session.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            return [row[0] for row in tables]
        #cursor = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #tables =  [row[0] for row in cursor.fetchall()]
        #return tables

    def list_account_configs(self) -> list[AccountConfig]:
        with Session(self.engine) as session:
            account_configs = session.query(AccountConfig).all()
            return account_configs
        #cursor = self.connection.execute("SELECT id, account_id, metatrader_id FROM ACCOUNT_CONFIG;")
        #account_configs = [AccountConfig(id=row[0], account_id=row[1], metatrader_id=row[2]) for row in cursor.fetchall()]
        return account_configs
    
    def countAccounts(self) -> int:
        with Session(self.engine) as session:
            count = session.query(AccountConfig).count()
            return count
        #cursor = self.connection.execute("SELECT COUNT(*) FROM ACCOUNT_CONFIG;")
        #count = cursor.fetchone()[0]
        #return count

    def listMetatraders(self) -> list[MetatraderConfig]:
        with Session(self.engine) as session:
            metatraders = session.query(MetatraderConfig).all()
            return metatraders
        #cursor = self.connection.execute("SELECT id, path FROM METATRADER_CONFIG;")
        #metatraders = [MetatraderConfig(id=row[0], path=row[1]) for row in cursor.fetchall()]
        #return metatraders

    def countMetatraders(self) -> int:
        with Session(self.engine) as session:
            count = session.query(MetatraderConfig).count()
            return count
        #cursor = self.connection.execute("SELECT COUNT(*) FROM METATRADER_CONFIG;")
        #count = cursor.fetchone()[0]
        #return count

    def addMetatrader(self, metatraderConfig: MetatraderConfig) -> int:
        with Session(self.engine) as session:
            session.add(metatraderConfig)
            session.commit()
            return metatraderConfig.id
        #cursor = self.connection.execute("""
        #    INSERT INTO METATRADER_CONFIG (path) VALUES (?);
        #""", (metatraderConfig.path,))
        #last_row_id = cursor.lastrowid
        #self.connection.commit()
        #return last_row_id

    def getMetatradersByPath(self, metatraderPath: str) -> list[MetatraderConfig]:
        with Session(self.engine) as session:
            metatraders = session.query(MetatraderConfig).filter(MetatraderConfig.path == metatraderPath).all()
            return metatraders
        #cursor = self.connection.execute("""
        #    SELECT id, path FROM METATRADER_CONFIG WHERE path = ?;
        #""", (metatraderPath,))
        #rows = cursor.fetchall()
        #console.print(f"Found {len(rows)} metatrader(s) with path: {metatraderPath}")
        #return [MetatraderConfig(id=row[0], path=row[1]) for row in rows]
    
    def deleteMetatrader(self, metatraderId: int) -> None:
        with Session(self.engine) as session:
            metatrader = session.query(MetatraderConfig).filter(MetatraderConfig.id == metatraderId).first()
            if bool(metatrader):
                session.delete(metatrader)
                session.commit()
        #self.connection.commit()
        #console.print(f"Deleted metatrader with ID: {metatraderId}")

    def accounts(self) -> list[AccountConfig]:
        with Session(self.engine) as session:
            accounts = session.query(AccountConfig).all()
            return accounts
        #"""List all accounts."""
        #return []
    

    