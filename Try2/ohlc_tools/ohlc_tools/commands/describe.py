"""
ohlc_tools.commands.describe
============================

`ohlc describe` — print a summary of an OHLC CSV file.

Usage
-----
    ohlc describe path/to/file.csv
    ohlc describe path/to/file.csv --no-color
"""

from __future__ import annotations

import os
import click
from rich.console import Console
from rich.table import Table
from rich import box

from ohlc_tools.utils.csv_reader import load_data
from ohlc_tools.utils.timeframe import detect_timeframe
from ohlc_tools.utils.display import human_size, format_datetime

console = Console()


def _build_summary(filepath: str) -> dict:
    """Load an OHLC file and return a summary dict."""
    file_size = os.path.getsize(filepath)
    df = load_data(filepath)

    timestamps = df.index.sort_values()
    tz = str(timestamps.tzinfo) if timestamps.tzinfo is not None else "Unknown"
    timeframe = detect_timeframe(timestamps)

    return {
        "file":      os.path.basename(filepath),
        "size":      human_size(file_size),
        "size_raw":  file_size,
        "rows":      len(df),
        "timeframe": timeframe,
        "timezone":  tz,
        "start":     format_datetime(timestamps.min()),
        "end":       format_datetime(timestamps.max()),
        "columns":   list(df.columns),
    }


@click.command()
@click.argument("filepath", type=click.Path(exists=True, dir_okay=False))
@click.option("--no-color", is_flag=True, default=False,
              help="Disable Rich colour output (plain text).")
def cli(filepath: str, no_color: bool) -> None:
    """Print a structured summary of an OHLC CSV file.

    FILEPATH  Path to the CSV file containing OHLC data.
    """
    con = Console(highlight=not no_color, markup=not no_color)

    try:
        summary = _build_summary(filepath)
    except Exception as exc:  # noqa: BLE001
        con.print(f"[bold red]Error:[/] {exc}")
        raise SystemExit(1) from exc

    table = Table(
        title=f"[bold cyan]OHLC Summary — {summary['file']}[/]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        expand=False,
    )
    table.add_column("Property",  style="bold", min_width=18)
    table.add_column("Value",     min_width=30)

    table.add_row("File size",  f"{summary['size']}  ({summary['size_raw']:,} bytes)")
    table.add_row("Timeframe",  summary["timeframe"])
    table.add_row("Timezone",   summary["timezone"])
    table.add_row("Start date", summary["start"])
    table.add_row("End date",   summary["end"])
    table.add_row("Total rows", f"{summary['rows']:,}")
    table.add_row("Columns",    ", ".join(summary["columns"]))

    con.print()
    con.print(table)
    con.print()


if __name__ == "__main__":
    cli()
