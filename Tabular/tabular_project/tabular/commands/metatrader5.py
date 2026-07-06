import click
import os
from rich.console import Console
from tabular.util.fileutils import pick_file
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.util.xmlutils import load_xml_config

CONFIG_SUB_COMMANDS: list[tuple[str, str | None]] = [
    ['Append a MT5', 'appendMT5'], 
    ['delete', 'delete'], 
    ['list', 'list'], 
    ['Return to previous menu', None]
]

console = Console()
databaseService: DatabaseService = None

@click.command()
def appendMT5():
    """ Select a MetaTrader 5 installation"""
    metatraderPath = pick_file(start_dir=os.getcwd())
    if bool(metatraderPath) and metatraderPath.endswith(".exe") and len(databaseService.getMetatradersByPath(metatraderPath)) == 0:
        metatraderId = databaseService.addMetatrader(metatraderPath)



@click.group()
def metatrader5():
    """ Load the configuration from the XML file.  """
    config = SingletonService().get("config")
    if config is not None and not config.endswith(".xml"):
        click.echo("❌ Error: file must be an .xml file.")
        config = None
    if config is None:
        click.echo(f"No config file provided. You can specify one with 'tabular [CONFIG]'.")
        config = pick_file(start_dir=os.getcwd())

    databaseService = DatabaseService()

    click.echo(f"Selected config file: {config}")
    accounts = load_xml_config(config)
    SingletonService().put("accounts", accounts)

metatrader5.add_command(appendMT5)