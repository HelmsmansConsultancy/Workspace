
from dataclasses import dataclass

@dataclass
class CsvFile:
    filename: str
    filesize: int
    delimiter: str
    timestamp: str
    columns: list[str]
