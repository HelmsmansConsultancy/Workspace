from rich.console import Console

console = Console()

class DatabaseService():
    path: str

    def __init__(self):
        self.console = Console()