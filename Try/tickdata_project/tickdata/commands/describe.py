from email.policy import default
import os
import csv
from typing import Required
import click
from rich.console import Console
from rich.table import Table
from rich import box
from prompt_toolkit import prompt
from tickdata.data.csvfile import CsvFile
from tickdata.util.csvutils import load_tickdata
from tickdata.util.display import human_size, format_datetime
from tickdata.util.filecompletion import prompt_filename

console = Console()

@click.command()
@click.argument("source", default=None, required=False, type=click.Path(exists=False))
def describe(source):
    """Describe the contents of FILENAME."""
    if source is None:
        source = prompt_filename('Enter file to describe')

    click.echo(f"Describing: {source}")
    csvFile = load_tickdata(source)
    
    table = Table(
        title=f"[bold cyan]Tickdata Summary — {csvFile.filename}[/]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        expand=False,
    )
    table.add_column("Property",  style="bold", min_width=18)
    table.add_column("Value",     min_width=30)

    table.add_row("File size",  f"{human_size(csvFile.filesize)}")
    table.add_row("Timeframe",  "Tick Data")
    table.add_row("Start date", format_datetime(csvFile.df["DateTime"].min()))
    table.add_row("End date",   format_datetime(csvFile.df["DateTime"].max()))
    table.add_row("Total rows", f"{csvFile.df["DateTime"].count()}")
    table.add_row("Columns",    ", ".join(csvFile.df.columns))

    console.print()
    console.print(table)
    console.print()

