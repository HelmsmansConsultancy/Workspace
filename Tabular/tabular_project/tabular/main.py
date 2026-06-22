import click
import questionary
import os
from rich.console import Console
from tabular.commands.connect import connect

SUBCOMMANDS = ['connect'] 

console = Console()

def interactive_menu():
    click.echo("What do you want to do?")
    for i, name in enumerate(SUBCOMMANDS, 1):
        click.echo(f"  {i}. {name}")
    idx = click.prompt(
        "Enter number",
        type=click.IntRange(1, len(SUBCOMMANDS))
    )
    return SUBCOMMANDS[idx - 1]

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
            else:
                choices.append(f"📄 {entry}")

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

#@click.group(invoke_without_command=True)
#@click.pass_context
@click.command()
@click.option("--config", "config", default=None, help="Path to the file to process")
def main(config):
    """Tabular MT5 data management tool."""
    click.echo("Tabular starting...")
    if config is None:
        click.echo(f"No config file provided. You can specify one with 'tabular [CONFIG]'.")
        config = pick_file(start_dir=os.getcwd())
    click.echo(f"Selected config file: {config}")


        #source = prompt_with_completion('Enter file to analyze: ')
#    if ctx.invoked_subcommand is None:
#        choice = interactive_menu()
#        ctx.invoke(ctx.command.commands[choice])

#main.add_command(connect)

if __name__ == "__main__":
    main()