import click
import os
from rich.console import Console
from tabular.commands.exit import exit
from tabular.commands.config import config
from tabular.commands.connect import connect
from tabular.commands.db import db
from tabular.commands.list import list 
from tabular.util.xmlutils import load_xml_config
from tabular.util.menuutils import interactive_menu
from tabular.util.fileutils import pick_file
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.data.application_config import ApplicationConfig

SUB_COMMANDS: list[tuple[str, str | None]] = [
    ['Config', 'config'], 
    ['Connect', 'connect'], 
    ['DB', 'db'], 
    ['List', 'list'], 
    ['Load', 'load'], 
    ['Exit nicely', 'exit']
]

console = Console()

@click.group(invoke_without_command=True)
@click.option(
    "--db_file",
    "db_file",
    type=click.Path(),
    default=None,  # resolved lazily below so it reflects sys.argv[0] correctly
    help="Path to the SQLite database file. Defaults to <script_name>.db",
)
@click.pass_context
def main(ctx: click.Context, db_file: str):
    """Tabular MT5 data management tool."""
    applicationConfig    = ApplicationConfig()

    if bool(db_file) and db_file.endswith(".db"):
        applicationConfig.db_file = db_file
    SingletonService().put("ApplicationConfig", applicationConfig)
    databaseService = DatabaseService()

    click.echo("Tabular starting...")
    start_dir=os.getcwd()
    SingletonService().put("start_dir", start_dir)

    accounts = databaseService.accounts()
    SingletonService().put("accounts", accounts)

    while True:
        click.echo(f"Managing {len(accounts)} account(s)")
        if ctx.invoked_subcommand is None:
            choice = interactive_menu(SUB_COMMANDS)
            ctx.invoke(ctx.command.commands[choice])

main.add_command(config)
main.add_command(connect)
main.add_command(db)
main.add_command(list)
main.add_command(exit)

if __name__ == "__main__":
    main()