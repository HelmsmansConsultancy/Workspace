import click
from rich.console import Console
from tickdata.data.csvfile import CsvFile
from tickdata.util.csvutils import load_tickdata
from tickdata.util.filecompletion import prompt_with_completion

console = Console()

@click.command()
@click.argument("source", default=None, required=False, type=click.Path(exists=False))
def analyze(source):
    """Analyze the contents of FILENAME."""
    if source is None:
        source = prompt_with_completion('Enter file to analyze: ')

    click.echo(f"Analyzing: {source}")
    csvFile = load_tickdata(source)
    csvFile.df['difference'] = csvFile.df['timestamp'].diff().dt.total_seconds()
    
    table = Table(
        title=f"[bold cyan]Tickdata Summary — {csvFile.filename}[/]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        expand=False,
    )
