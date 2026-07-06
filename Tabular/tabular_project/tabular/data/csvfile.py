
from dataclasses import dataclass
import pandas as pd

@dataclass
class CsvFile:
    filename: str
    filesize: int
    delimiter: str
    timestamp: str
    ask: str
    bid: str
    columns: list[str]
    df: pd.DataFrame


    def __init__(self):
        pass

