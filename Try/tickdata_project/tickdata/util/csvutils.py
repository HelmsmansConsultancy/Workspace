import csv
from pathlib import Path
from rich.console import Console
from tickdata.data import CsvFile

import pandas as pd

console = Console()

def _sniff_delimiter(filepath: str) -> str:
    """Return the most likely delimiter by inspecting the first 8 KB."""
    with open(filepath, newline="", encoding="utf-8-sig") as fh:
        sample = fh.read(8192)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        console.print(f"Found delimiter {dialect.delimiter}")
        return dialect.delimiter
    except csv.Error:
        return ","

def _find_ts_column(columns: list[str]) -> str | None:
    """Return the name of the timestamp column, or None."""
    for col in columns:
        if col.strip().lower() in _TS_COLUMN_NAMES:
            console.print(f"Found timestamp column {col}")
            return col
    return columns[0] if columns else None

def load_tickdata(filepath: str | Path) -> CsvFile:
    """Load a CSV file and return a DataFrame with a DatetimeIndex.

    Parameters
    ----------
    filepath : str | Path
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame indexed by datetime, with at minimum Bid / Ask
        columns.  Column names are preserved as-is from the source file.

    Raises
    ------
    FileNotFoundError
        If *filepath* does not exist.
    ValueError
        If no valid timestamp column or OHLC columns can be found.
    """
    csv = CsvFile()
    csv.filepath = str(filepath)
    csv.filesize = os.path.getsize(filepath)
    csv.delimiter = _sniff_delimiter(filepath)
    csv.df = pd.read_csv(csv.filepath, sep=csv.delimiter, encoding="utf-8-sig", low_memory=False)
    csv.columns = list(csv.df.columns.str.strip())
    console.print(f"Found columns: {', '.join(csv.df.columns)}")

    csv.timestamp = _find_ts_column(csv.columns)



