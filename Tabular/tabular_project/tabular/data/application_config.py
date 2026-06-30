import os
from dataclasses import dataclass

@dataclass
class ApplicationConfig:
    db_file: str


    def __init__(self):
        self.db_file = os.getcwd()  + ".db"
    



