
from dataclasses import dataclass
import pandas as pd

@dataclass
class CsvFile:
    filename: str
    filesize: int
    delimiter: str
    timestamp: str
    columns: list[str]
    df: pd.DataFrame
