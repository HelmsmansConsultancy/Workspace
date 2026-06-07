import csv

import click
from rich.table import Table
from rich import box
from tickdata.data.csvfile import CsvFile
from tickdata.util.csvutils import load_tickdata
from tickdata.util.display import human_size, format_datetime

@click.command()
@click.argument("filename", type=click.Path(exists=True))
def describe(filename):
    """Describe the contents of FILENAME."""
    click.echo(f"Describing: {filename}")
    # TODO: implement describe logic
    csvFile = load_tickdata(filename)
    

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
    table.add_row("Start date", format_datetime(csvFile.df.min()))
    table.add_row("End date",   format_datetime(csvFile.df.max()))
    table.add_row("Total rows", f"{summary['rows']:,}")
    table.add_row("Columns",    ", ".join(summary["columns"]))

    con.print()
    con.print(table)
    con.print()

