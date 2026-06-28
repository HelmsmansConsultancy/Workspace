import click
import os
from rich.console import Console 


console = Console()


def list_files(filepath):

    # Get the directory the file lives in
    directory = os.path.dirname(filepath)

    # List all files in that directory
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path):
            console.print(f"📁 {entry}")
        else:
            console.print(f"📄 {entry}")