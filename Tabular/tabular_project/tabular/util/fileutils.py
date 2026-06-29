import click
import questionary
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

def get_dirs(path: str) -> list[str]:
    """Returns subdirectories sorted alphabetically."""
    entries = os.listdir(path)
    return sorted([e for e in entries if os.path.isdir(os.path.join(path, e))])


def determine_new_file(current_path: str) -> str | None:
    """
    Interactive directory navigator.
    Returns the full path of the new file, or None if the user quits.
    """
    while True:
        dirs = get_dirs(current_path)

        click.clear()
        click.echo(f"\n📁  {current_path}\n")

        options: list[tuple[str, str]] = []  # (label, full_path)

        # Parent directory option (unless at root)
        if current_path != os.path.abspath(os.sep):
            options.append((".. (go up)", os.path.dirname(current_path)))

        # Subdirectories
        for d in dirs:
            options.append((f"📁  {d}/", os.path.join(current_path, d)))

        # Display numbered list
        for i, (label, _) in enumerate(options, 1):
            click.echo(f"  {i}. {label}")

        click.echo(f"  {len(options) + 1}. ✅  Select this directory")
        click.echo(f"  {len(options) + 2}. ❌  Quit\n")

        choices = [str(i) for i in range(1, len(options) + 3)]
        choice = click.prompt("Choose", type=click.Choice(choices), show_choices=False)
        idx = int(choice) - 1

        # Quit
        if idx == len(options) + 1:
            return None

        # Confirm current directory — prompt for filename
        if idx == len(options):
            click.echo(f"\n  📁  Saving to: {current_path}")
            filename = click.prompt("  Enter new filename")
            return os.path.join(current_path, filename)

        # Navigate into subdirectory
        _, selected_path = options[idx]
        current_path = selected_path

def pick_file(start_dir):
    current_dir = os.path.abspath(start_dir)

    while True:
        # Build list of choices
        entries = sorted(os.listdir(current_dir))
        choices = [".. (go up)"]

        for entry in entries:
            full_path = os.path.join(current_dir, entry)
            if os.path.isdir(full_path):
                choices.append(f"📁 {entry}")
            elif entry.endswith(".xml"):
                choices.append(f"📄 {entry}")
            else:
                # Visible but greyed out and not selectable
                choices.append(questionary.Choice(f"📄 {entry}", disabled="not an XML file"))

        # Show current directory and prompt
        selection = questionary.select(
            f"📂 {current_dir}\nSelect a file or navigate:",
            choices=choices
        ).ask()

        # User cancelled (Ctrl+C)
        if selection is None:
            return None

        # Go up a directory
        if selection == ".. (go up)":
            current_dir = os.path.dirname(current_dir)
            continue

        # Strip the icon prefix to get the real name
        name = selection[2:].strip()
        full_path = os.path.join(current_dir, name)

        if os.path.isdir(full_path):
            # Navigate into directory
            current_dir = full_path
        else:
            # File selected
            return full_path

def get_dir_contents(path: str) -> tuple[list[str], list[str]]:
    """Returns (dirs, files) sorted alphabetically."""
    entries = os.listdir(path)
    dirs = sorted([e for e in entries if os.path.isdir(os.path.join(path, e))])
    files = sorted([e for e in entries if os.path.isfile(os.path.join(path, e))])
    return dirs, files


def navigate_menu(current_path: str) -> str | None:
    """
    Interactive directory navigator.
    Returns a file path when a file is selected, or None if the user quits.
    """
    while True:
        dirs, files = get_dir_contents(current_path)

        click.clear()
        click.echo(f"\n📁  {current_path}\n")

        options: list[tuple[str, str]] = []  # (label, full_path)

        # Parent directory option (unless at root)
        if current_path != os.path.abspath(os.sep):
            options.append((".. (go up)", os.path.dirname(current_path)))

        # Subdirectories
        for d in dirs:
            options.append((f"📁  {d}/", os.path.join(current_path, d)))

        # Files
        for f in files:
            options.append((f"📄  {f}", os.path.join(current_path, f)))

        # Display numbered list
        for i, (label, _) in enumerate(options, 1):
            click.echo(f"  {i}. {label}")

        click.echo(f"  {len(options) + 1}. ✏️  Type a filename manually")
        click.echo(f"  {len(options) + 2}. ❌  Quit\n")

        choices = [str(i) for i in range(1, len(options) + 3)]
        choice = click.prompt("Choose", type=click.Choice(choices), show_choices=False)
        idx = int(choice) - 1

        # Quit
        if idx == len(options) + 1:
            return None

        # Manual filename entry
        if idx == len(options):
            filename = click.prompt("Enter filename")
            full_path = os.path.join(current_path, filename)
            if os.path.isfile(full_path):
                return full_path
            else:
                click.echo(click.style(f"\n  ⚠️  File not found: {full_path}", fg="yellow"))
                click.pause()
            continue

        # Directory or file selected
        label, selected_path = options[idx]

        if os.path.isdir(selected_path):
            current_path = selected_path  # Navigate into directory
        elif os.path.isfile(selected_path):
            return selected_path          # Return the chosen file
