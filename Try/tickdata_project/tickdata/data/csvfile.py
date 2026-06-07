
from dataclasses import dataclass

@dataclass
class CsvFile:
    filepath: str
    filesize: int
    delimiter: str
    timestamp: str
    columns: list[str]

