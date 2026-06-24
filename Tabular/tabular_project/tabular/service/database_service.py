import sqlite3
from rich.console import Console


class DatabaseService():
    def __init__(self, start_dir):
        self.console = Console()

    def accounts(self):
        """List all accounts."""
        self.console.print("Listing all accounts...")
        return None
    