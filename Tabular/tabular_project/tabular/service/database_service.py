import sqlite3
from sqlite3 import Connection
from typing import cast
from rich.console import Console
from tabular.data.account_config import AccountConfig
from tabular.service.singleton_service import SingletonService


class DatabaseService():
    connection: Connection

    def __init__(self):
        self.console = Console()
        db_file = cast(AccountConfig, SingletonService().get("ApplicationConfig")).db_file
        self.console.print(f"Starting database at: {db_file}")
        connection = sqlite3.connect(db_file)

    def accounts(self) -> list[AccountConfig]:
        """List all accounts."""
        return []
    