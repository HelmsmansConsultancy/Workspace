"""
ohlc_tools.commands.resample
=============================

`ohlc resample` — resample OHLC data to a coarser timeframe.

Usage
-----
    ohlc resample eurusd_h1.csv --timeframe H4 --output eurusd_h4.csv
    ohlc resample eurusd_m1.csv --timeframe D  --output eurusd_daily.csv
"""

from __future__ import annotations

import click
import pandas as pd
from rich.console import Console

from ohlc_tools.utils.csv_reader import load_data
from ohlc_tools.utils.timeframe import PANDAS_FREQ_ALIASES


console = Console()


def _resample_ohlc(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    """Resample a standard OHLC DataFrame to *rule* (pandas offset alias)."""
    # Normalise column names to lowercase for reliable access
    df.columns = [c.lower() for c in df.columns]

    required = {"open", "high", "low", "close"}
    missing  = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing OHLC columns: {', '.join(sorted(missing))}")

    agg: dict[str, str | pd.NamedAgg] = {
        "open":  "first",
        "high":  "max",
        "low":   "min",
        "close": "last",
    }

    if "volume" in df.columns:
        agg["volume"] = "sum"

    resampled = df.resample(rule).agg(agg).dropna(subset=["open"])
    return resampled


@click.command()
@click.argument("filepath", type=click.Path(exists=True, dir_okay=False))
@click.option("-t", "--timeframe", required=True,
              type=click.Choice(list(PANDAS_FREQ_ALIASES.keys()), case_sensitive=False),
              help="Target timeframe.")
@click.option("-o", "--output", required=True,
              type=click.Path(dir_okay=False, writable=True),
              help="Output CSV file path.")
@click.option("--delimiter", default=",", show_default=True,
              help="Output CSV delimiter.")
def cli(filepath: str, timeframe: str, output: str, delimiter: str) -> None:
    """Resample an OHLC CSV file to a coarser timeframe.

    FILEPATH  Path to the source CSV file.

    Available timeframes: M1 M5 M15 M30 H1 H2 H4 H8 D W M
    """
    rule = PANDAS_FREQ_ALIASES[timeframe.upper()]

    try:
        df      = load_data(filepath)
        result  = _resample_ohlc(df, rule)
        result.to_csv(output, sep=delimiter)

        console.print(
            f"[green]✓[/] Resampled [bold]{filepath}[/] → [bold]{output}[/]\n"
            f"   Timeframe : {timeframe.upper()}\n"
            f"   Input rows: {len(df):,}   →   Output rows: {len(result):,}"
        )
    except Exception as exc:  # noqa: BLE001
        console.print(f"[bold red]Error:[/] {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    cli()
