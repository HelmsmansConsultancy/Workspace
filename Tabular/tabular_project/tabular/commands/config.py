import click
from rich.console import Console
from tabular.service.singleton_service import SingletonService
from tabular.util.xmlutils import load_xml_config


console = Console()

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


@click.command()
def config():
    """ Load the configuration from the XML file.  """
    config = SingletonService().get("config")
    if config is not None and not config.endswith(".xml"):
        click.echo("❌ Error: file must be an .xml file.")
        config = None
    if config is None:
        click.echo(f"No config file provided. You can specify one with 'tabular [CONFIG]'.")
        config = pick_file(start_dir=os.getcwd())

    click.echo(f"Selected config file: {config}")
    accounts = load_xml_config(config)
    SingletonService().put("accounts", accounts)