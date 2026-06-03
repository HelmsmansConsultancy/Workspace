"""
ohlc_tools.utils.csv_reader
============================

Auto-detecting CSV loader that returns a pandas DataFrame with a
DatetimeIndex.  Handles a wide variety of real-world OHLC file formats.
"""

from __future__ import annotations

import re
import csv
from pathlib import Path
from rich.console import Console

import pandas as pd


# Columns we accept as the timestamp / date column
_TS_COLUMN_NAMES = {
    "date", "time", "datetime", "timestamp",
    "open_time", "opentime", "close_time", "closetime",
    "date_time", "bar_time",
}

_COMMON_FORMATS = [
    "%Y%m%d %H:%M:%S.%f",
"""
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%d",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%Y",
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y",
"""
]

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
            console.print(f"Found Timestamp column {col}")
            return col
    return columns[0] if columns else None


def _parse_timestamps(series: pd.Series) -> pd.DatetimeIndex:
    """Try to parse a Series of strings as datetimes, return DatetimeIndex."""
    # Try pandas auto-detection first (handles ISO 8601 + many others)
    try:
        return pd.to_datetime(series, utc=False, infer_datetime_format=True)
    except Exception:
        pass

    # Try unix timestamps (numeric strings)
    if series.dtype in (float, int) or series.str.fullmatch(r"-?\d+(\.\d+)?").all():
        numeric = pd.to_numeric(series, errors="coerce")
        if numeric.max() > 1e12:          # milliseconds
            return pd.to_datetime(numeric, unit="ms", utc=True)
        return pd.to_datetime(numeric, unit="s", utc=True)

    # Brute-force through known format strings
    for fmt in _COMMON_FORMATS:
        try:
            return pd.to_datetime(series, format=fmt)
        except Exception:
            continue

    raise ValueError(
        "Could not parse timestamp column. "
        "Please ensure the file contains a recognisable date/time format."
    )


def load_data(filepath: str | Path) -> pd.DataFrame:
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
    filepath = str(filepath)
    sep = _sniff_delimiter(filepath)

    df = pd.read_csv(filepath, sep=sep, encoding="utf-8-sig", low_memory=False)
    df.columns = df.columns.str.strip()
    console.print(f"Found columns: {', '.join(df.columns)}")

    if df.empty:
        raise ValueError("The CSV file is empty.")

    # ── Parse timestamps ──────────────────────────────────────────────────
    ts_col = _find_ts_column(list(df.columns))
    if ts_col is None:
        raise ValueError("No suitable timestamp column found.")

    df.index = _parse_timestamps(df[ts_col].astype(str))
    df.index.name = "DateTime"
    df.drop(columns=[ts_col], inplace=True)

    return df
