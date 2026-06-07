import os
import csv
import click
from rich.console import Console
from rich.table import Table
from rich import box
from tickdata.data.csvfile import CsvFile
from tickdata.util.csvutils import load_tickdata
from tickdata.util.display import human_size, format_datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

class FileCompleter(Completer):
    """Tab-completes filenames and directories."""

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        dirname = os.path.dirname(text)
        prefix = os.path.basename(text)
        search_dir = dirname if dirname else '.'

        try:
            entries = sorted(os.listdir(search_dir))
        except OSError:
            return

        for entry in entries:
            if entry.startswith(prefix):
                full = os.path.join(dirname, entry) if dirname else entry
                suffix = os.sep if os.path.isdir(full) else ''
                yield Completion(
                    entry + suffix,
                    start_position=-len(prefix),
                    display_meta='dir' if os.path.isdir(full) else 'file'
                )

def prompt_filename(message='Enter filename'):
    """Prompt for a filename with tab-autocomplete."""
    return prompt(
        f'{message}: ',
        completer=FileCompleter(),
        complete_while_typing=True,  # show completions as you type
    )

console = Console()

def complete_filename(text, state):
    """Tab-completes filenames using os module."""
    dirname = os.path.dirname(text)
    prefix = os.path.basename(text)
    search_dir = dirname if dirname else '.'

    try:
        entries = os.listdir(search_dir)
    except OSError:
        return None

    matches = []
    for entry in entries:
        if entry.startswith(prefix):
            full = os.path.join(dirname, entry) if dirname else entry
            # append slash to directories so you can keep tabbing into them
            if os.path.isdir(full):
                full += os.sep
            matches.append(full)

    return matches[state] if state < len(matches) else None

@click.command()
@click.argument("filename", type=click.Path(exists=False))
def describe(filename):
    """Describe the contents of FILENAME."""
    if filename is None:
        filename = prompt_filename('Enter file to deploy')

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
    table.add_row("Start date", format_datetime(csvFile.df["DateTime"].min()))
    table.add_row("End date",   format_datetime(csvFile.df["DateTime"].max()))
    table.add_row("Total rows", f"{csvFile.df["DateTime"].count()}")
    table.add_row("Columns",    ", ".join(csvFile.df.columns))

    console.print()
    console.print(table)
    console.print()

