"""
ohlc_tools.commands.convert
============================

`ohlc convert` — convert an OHLC CSV file to a different delimiter or column order.

Usage
-----
    ohlc convert input.csv --delimiter ";" --output output.csv
    ohlc convert input.csv --delimiter "\\t" --output output.tsv
"""

from __future__ import annotations

import click
from rich.console import Console

from ohlc_tools.utils.csv_reader import load_data


console = Console()

DELIMITER_ALIASES = {
    "tab":  "\t",
    "\\t":  "\t",
    "semi": ";",
    "pipe": "|",
}


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
    """Convert an OHLC CSV file to a different delimiter format.

    FILEPATH  Path to the source CSV file.
    """
    sep = DELIMITER_ALIASES.get(delimiter.lower(), delimiter)

    try:
        df = load_data(filepath)
        df.to_csv(output, sep=sep, index=not no_index)
        console.print(f"[green]✓[/] Converted [bold]{filepath}[/] → [bold]{output}[/]"
                      f"  (delimiter={repr(sep)}, rows={len(df):,})")
    except Exception as exc:  # noqa: BLE001
        console.print(f"[bold red]Error:[/] {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    cli()
