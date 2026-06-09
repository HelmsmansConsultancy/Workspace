"""
ohlc_tools.commands.tobar
============================

`ohlc describe` — print a summary of an OHLC CSV file.

Usage
-----
    ohlc tobar path/to/file.csv --output output.csv
    ohlc tobar path/to/file.csv --no-color --output output.csv
"""

from __future__ import annotations

import os
import click
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box
from ohlc_tools.utils.csv_reader import load_data


console = Console()


@click.command()
@click.argument("filepath", type=click.Path(exists=True, dir_okay=False))
@click.option("-d", "--delimiter", default=",", show_default=True,
              help="Output column delimiter (e.g. ',' ';' 'tab' '|').")
@click.option("-o", "--output", required=True,
              type=click.Path(dir_okay=False, writable=True),
              help="Output file path.")
@click.option("--no-index", is_flag=True, default=False,
              help="Omit the timestamp index column from the output.")
def cli(filepath: str, delimiter: str, output: str, no_index: bool) -> None:
    """Convert an Bid / Ask CSV file to a OHLC format.

    FILEPATH  Path to the input CSV file.
    OUTPUT  Path to the output CSV file.
    """

    try:
        df = load_data(filepath)
        
        # ── Validate required columns ─────────────────────────────────────────
        required = {"bid", "ask", "volume"}
        missing = required - set(df.columns)
        print(f"Found index column: {df.index.name}")
        if df.index.name != "datetime":
            missing.add("datetime")
        if missing:
            missingColumns = ', '.join(sorted(missing))
            presentColums = ', '.join(sorted(df.columns))
            raise ValueError(f"Missing OHLC columns: {missingColumns} only found {presentColums}")

        
        # ── Parse numeric columns ─────────────────────────────────────────────
        for col in ("bid", "ask", "volume"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        
        n_bad = df[["bid", "ask"]].isna().any(axis=1).sum()
        if n_bad:
            print(f"      WARNING: Dropping {n_bad:,} rows with invalid Bid/Ask values.")
            df = df.dropna(subset=["bid", "ask"])
        
        bars = resample_to_1m(df)
        
        save_bars(bars, output)

    finally:
        console.print("Okay")


def resample_to_1m(ticks: pd.DataFrame) -> pd.DataFrame:
    print("Resampling to 1-minute bars ...")
    ## ticks = ticks.set_index("DateTime")

    bars = pd.DataFrame()
    bars["ask_open"]       = ticks["ask"].resample("1min").first()
    bars["ask_high"]       = ticks["ask"].resample("1min").max()
    bars["ask_low"]        = ticks["ask"].resample("1min").min()
    bars["ask_close"]      = ticks["ask"].resample("1min").last()
    bars["bid_open"]       = ticks["bid"].resample("1min").first()
    bars["bid_high"]       = ticks["bid"].resample("1min").max()
    bars["bid_low"]        = ticks["bid"].resample("1min").min()
    bars["bid_close"]      = ticks["bid"].resample("1min").last()
    bars["volume"]         = ticks["volume"].resample("1min").sum()
    bars["tick_count"]     = ticks["timestamp"].resample("1min").count()
    bars["timestamp"]      = ticks["timestamp"].resample("1min").first()

    # Drop empty bars
    bars = bars[bars["tick_count"] > 0].reset_index()
    ## bars.rename(columns={"DateTime": "datetime"}, inplace=True)

    print(f"      Generated {len(bars):,} 1-minute bars "
          f"(from {bars['datetime'].iloc[0]} to {bars['datetime'].iloc[-1]})")
    return bars

def save_bars(bars: pd.DataFrame, path: str) -> None:
    print(f"[4/4] Saving bars to '{path}' ...")
    bars.to_csv(path, index=False, float_format="%.8g")
    print(f"      Done. {len(bars):,} bars written.")

if __name__ == "__main__":
    cli()