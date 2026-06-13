import csv
import os
from pathlib import Path
from rich.console import Console
from tickdata.data.csvfile import CsvFile

import pandas as pd

console = Console()

_TS_COLUMN_NAMES = [
    "date", "time", "datetime", "timestamp", "TimeStamp", "DateTime"
]

_ASK_COLUMN_NAMES = [ "Ask", "ask" ]

_BID_COLUMN_NAMES = [ "Bid", "bid" ]

_COMMON_FORMATS = [
    "%Y%m%d %H:%M:%S.%f",
]

TIMESTAMP_COLUMN = "TimeStamp"
ASK_COLUMN = "Ask"
BID_COLUMN = "Bid"

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

def _find_ts_column(columns: list[str]) -> str:
    return _find_column(_TS_COLUMN_NAMES, columns)

def _find_column(names: list[str], columns: list[str]) -> str:
    ##console.print(f"Finding any of the columnnames " + "'" + "', '".join(names) + "'" +
    ##              ", in the columnlist " + "'" + "', '".join(columns) + "'")
    for col in columns:
        for name in names:
            if col.find(name) >= 0:
                return col
    return  ""

def load_tickdata(filename: str ) -> CsvFile:
    """Load a CSV file and return a DataFrame with a DatetimeIndex.

    Parameters
    ----------
    filename : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame indexed by datetime, with at minimum Bid / Ask
        columns.  Column names are preserved as-is from the source file.

    Raises
    ------
    FileNotFoundError
        If *filename* does not exist.
    ValueError
        If no valid timestamp column or OHLC columns can be found.
    """
    csvFile = CsvFile("", 0, "", "", "", "", [], None)
    csvFile.filename = str(filename)
    csvFile.filesize = os.path.getsize(filename)
    csvFile.delimiter = _sniff_delimiter(filename)
    csvFile.df = pd.read_csv(csvFile.filename, sep=csvFile.delimiter, encoding="utf-8-sig", low_memory=False)
    console.print("Found columns: '" + "', '".join(csvFile.df.columns) + "'")

    ts_column = _find_ts_column(csvFile.df.columns)
    if ts_column:
        console.print(f"Found the index column '{ts_column}' ")
        csvFile.timestamp = ts_column
        if (ts_column != TIMESTAMP_COLUMN):
            console.print(f"Renaming '{ts_column}' into '{TIMESTAMP_COLUMN}' ")
            csvFile.df.rename(columns={ts_column: TIMESTAMP_COLUMN}, inplace=True) 
    else:
        console.print(f"Did not find '{TIMESTAMP_COLUMN}' Column")
        raise ValueError("Not found time stamp column")
    
    ask_column = _find_column(_ASK_COLUMN_NAMES, csvFile.df.columns)
    if ask_column:
        csvFile.ask = ask_column
        if (ask_column != ASK_COLUMN):
            console.print(f"Renaming '{ask_column}' into '{ASK_COLUMN}' ")
            csvFile.df.rename(columns={ask_column: ASK_COLUMN}, inplace=True) 
    else:
        console.print(f"Did not find '{ASK_COLUMN}' Column")
        raise ValueError("Not found ask column")
    
    bid_column = _find_column(_BID_COLUMN_NAMES, csvFile.df.columns)
    if bid_column:
        csvFile.bid = bid_column
        if (bid_column != BID_COLUMN):
            console.print(f"Renaming '{bid_column}' into '{BID_COLUMN}' ")
            csvFile.df.rename(columns={bid_column: BID_COLUMN}, inplace=True) 
    else:
        console.print(f"Did not find '{BID_COLUMN}' Column")
        raise ValueError("Not found ask column")
    
    csvFile.columns = list(csvFile.df.columns)

    return csvFile



