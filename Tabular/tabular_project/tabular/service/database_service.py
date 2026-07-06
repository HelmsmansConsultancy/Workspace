import sqlite3
from sqlite3 import Connection
from typing import cast
from rich.console import Console
from tabular.data.account_config import AccountConfig
from tabular.data.metatrader_config import MetatraderConfig
from tabular.service.singleton_service import SingletonService


class DatabaseService():
    db_file: str
    connection: Connection

    def __init__(self):
        self.console = Console()
        self.db_file = cast(AccountConfig, SingletonService().get("ApplicationConfig")).db_file
        self.console.print(f"Starting database at: {self.db_file}")
        self.connection = sqlite3.connect(self.db_file)

        cursor = self.connection
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS METATRADER_CONFIG (id INTEGER PRIMARY KEY, 
                           path TEXT NOT NULL)
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ACCOUNT_CONFIG (id INTEGER PRIMARY KEY, 
                           account_id TEXT NOT NULL,
                           metatrader_id INTEGER NOT NULL,
                           FOREIGN KEY(metatrader_id) REFERENCES METATRADER_CONFIG(id))
        """)

    def listTables(self) -> list[str]:
        cursor = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables =  [row[0] for row in cursor.fetchall()]
        return tables
    

    def addMetatrader(self, metatraderConfig: MetatraderConfig) -> int:
        
        cursor = self.connection
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS METATRADER_CONFIG (id INTEGER PRIMARY KEY, 
                           path TEXT NOT NULL)
        """)

    def getMetatradersByPath(self, metatraderPath: str) -> list[MetatraderConfig]:
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS METATRADER_CONFIG (id INTEGER PRIMARY KEY, 
                           path TEXT NOT NULL)
        """)

    def accounts(self) -> list[AccountConfig]:
        """List all accounts."""
        return []
    

    