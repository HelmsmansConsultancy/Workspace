import click
from rich.console import Console
from rich.table import Table
from rich import box
from tabular.data.csvfile import CsvFile
from tabular.util.csvutils import load_tabular
from tabular.util.display import human_size, format_datetime
from tabular.util.filecompletion import prompt_with_completion

console = Console()

@click.command()
@click.argument("source", default=None, required=False, type=click.Path(exists=False))
def describe(source):
    """Describe the contents of FILENAME."""
    if source is None:
        source = prompt_with_completion('Enter file to describe: ')

    click.echo(f"Describing: {source}")
    csvFile = load_tabular(source)
    
    table = Table(
        title=f"[bold cyan]Tabular Summary — {csvFile.filename}[/]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        expand=False,
    )
    table.add_column("Property",  style="bold", min_width=18)
    table.add_column("Value",     min_width=30)

    table.add_row("File size",  f"{human_size(csvFile.filesize)}")
    table.add_row("Timeframe",  "Tabular MT5")
    table.add_row("Start date", format_datetime(csvFile.df["TimeStamp"].min()))
    table.add_row("End date",   format_datetime(csvFile.df["TimeStamp"].max()))
    table.add_row("Total rows", f"{csvFile.df['TimeStamp'].count()}")
    table.add_row("Columns",    "'" + "', '".join(csvFile.df.columns) + "'")

    table2 = Table(
        title=f"[bold cyan]Tabular Summary — {csvFile.filename}[/]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        expand=False,
    )
    table2.add_column("Property",  style="bold", min_width=15)
    table2.add_column("Min",     min_width=15)
    table2.add_column("Median",     min_width=15)
    table2.add_column("Max",     min_width=15)

    table2.add_row("Ask", f"{csvFile.df['Ask'].min()}", f"{csvFile.df['Ask'].median()}", f"{csvFile.df['Ask'].max()}")
    table2.add_row("Bid", f"{csvFile.df['Bid'].min()}", f"{csvFile.df['Bid'].median()}", f"{csvFile.df['Bid'].max()}")

    console.print()
    console.print(table)
    console.print(table2)
    console.print()

