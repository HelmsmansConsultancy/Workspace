import click
import os
from pathlib import Path
import MetaTrader5 as meta_trader_5
from MetaTrader5 import TerminalInfo
from typing import Callable, Optional 
import psutil
from rich.console import Console
from tabular.service.s import S
from tabular.util.fileutils import pick_file
from tabular.util.menuutils import interactive_menu, empty_string
from tabular.service.singleton_service import SingletonService
from tabular.service.database_service import DatabaseService
from tabular.data.metatrader_config import MetatraderConfig
from tabular.util.xmlutils import load_xml_config

console = Console()
databaseService: DatabaseService = None

def explain_empty():
    return empty_string
    
@click.command()
def delete_mt5():
    """ Delete a MetaTrader 5 installation"""
    mt5_installations = databaseService.listMetatraders()
    if len(mt5_installations) == 0:
        click.echo("No MT5 installations found.")
        return

    click.echo("Select a MT5 installation to delete:")
    for index, mt5 in enumerate(mt5_installations, start=1):
        click.echo(f"{index}. {mt5}")

    choice = click.prompt("Enter the number of the MT5 installation to delete", type=int)
    if 1 <= choice <= len(mt5_installations):
        mt5_to_delete = mt5_installations[choice - 1]
        databaseService.deleteMetatrader(mt5_to_delete.id)
        click.echo(f"Deleted MT5 installation: {mt5_to_delete}")
    else:
        click.echo("Invalid choice. No MT5 installation deleted.")


@click.command()
def append_mt5():
    """ Select a MetaTrader 5 installation"""
    metatraderPath = pick_file(start_dir=os.getcwd(), file_extension=".exe")
    click.echo(f"Selected MT5 path: {metatraderPath}")
    if bool(metatraderPath) and metatraderPath.endswith(".exe") and len(databaseService.getMetatradersByPath(metatraderPath)) == 0:
        metatraderId = databaseService.addMetatrader(MetatraderConfig(path=metatraderPath, name=Path(metatraderPath).parent.name))
        click.echo(f"MT5 installation added with ID: {metatraderId} and path: {metatraderPath}")

@click.command()
def list_mt5():
    """ List all MetaTrader 5 installations"""
    mt5_installations = databaseService.listMetatraders()
    click.echo(empty_string)
    if len(mt5_installations) > 0:
        click.echo("MT5 Installations:")
        for mt5 in mt5_installations:
            click.echo(f"- {mt5!r}")
    else:
        click.echo("No MT5 installations found.")
    click.echo(empty_string)

@click.command()
def connect_mt5():
    """ Connect to a MetaTrader 5 installation"""
    click.echo(empty_string)
    mt5_installations: list[MetatraderConfig] = databaseService.listMetatraders()
    if len(mt5_installations) == 0:
        click.echo("No MT5 installations found.")
        return

    click.echo("Select a MT5 installation to connect to:")
    for index, mt5 in enumerate(mt5_installations, start=1):
        click.echo(f"{index}. {mt5}")

    choice = click.prompt("Enter the number of the MT5 installation to connect to", type=int)
    if 1 <= choice <= len(mt5_installations):
        # Snapshot PIDs before initialization
        before = {p.pid for p in psutil.process_iter(["pid", "name"])
                if p.info["name"] == "terminal64.exe"}
        
        mt5_to_connect: MetatraderConfig = mt5_installations[choice - 1]
        # Perform connection logic here
        meta_trader_5.initialize(path=mt5_to_connect.path)

        term_info: TerminalInfo | None = meta_trader_5.terminal_info()
        if term_info is None or not term_info.connected:
            click.echo(f"Terminal not connected to broker: {meta_trader_5.last_error()}")
        else:
            click.echo(f"Connected to MT5 installation: {mt5_to_connect.path}")
            SingletonService().put(S.CONNECTED_MT5, mt5_to_connect)

            if term_info.connected:
                if mt5_to_connect.trade_allowed is None or mt5_to_connect.tradeapi_disabled is None or mt5_to_connect.notifications_enabled is None or mt5_to_connect.mqid is None:
                    mt5_to_connect.trade_allowed = term_info.trade_allowed
                    mt5_to_connect.tradeapi_disabled = term_info.tradeapi_disabled
                    mt5_to_connect.notifications_enabled = term_info.notifications_enabled
                    mt5_to_connect.mqid = term_info.mqid
                    databaseService.updateMetatrader(mt5_to_connect)
                    click.echo(f"Updated MT5 permissions info")

                if mt5_to_connect.terminal_version is None or mt5_to_connect.build is None or mt5_to_connect.release_date is None:
                    version_info: Optional[tuple[int, int, str]] = meta_trader_5.version()
                    mt5_to_connect.terminal_version = f"{version_info[0]}.{version_info[1]} {version_info[2]}"
                    mt5_to_connect.build = version_info[1]
                    mt5_to_connect.release_date = version_info[2]
                    databaseService.updateMetatrader(mt5_to_connect)
                    click.echo(f"Updated MT5 version info")
        
        # Snapshot PIDs before initialization
        after = {p.pid for p in psutil.process_iter(["pid", "name"])
                if p.info["name"] == "terminal64.exe"}

        new_pids = after - before
        if new_pids:
            mt5_pid = new_pids.pop()
            print(f"MT5 started with PID {mt5_pid}")
            SingletonService().put(S.MT5_PID, mt5_pid)
        else:
            print("MT5 was already running; PID not tracked")

    else:
        click.echo("Invalid choice. No MT5 installation connected.")

@click.command()
def update_mt5():
    """ Update MetaTrader 5 installation info"""
    click.echo(empty_string)
    mt5_installations: list[MetatraderConfig] = databaseService.listMetatraders()
    if len(mt5_installations) == 0:
        click.echo("No MT5 installations found.")
        return

    click.echo("Select a MT5 installation to connect to:")
    for index, mt5 in enumerate(mt5_installations, start=1):
        click.echo(f"{index}. {mt5}")

    choice = click.prompt("Enter the number of the MT5 installation to connect to", type=int)
    if 1 <= choice <= len(mt5_installations):
        mt5_to_connect: MetatraderConfig = mt5_installations[choice - 1]
        # Perform connection logic here
        meta_trader_5.initialize(path=mt5_to_connect.path)

        term_info: TerminalInfo | None = meta_trader_5.terminal_info()
        if term_info is None or not term_info.connected:
            click.echo(f"Terminal not connected to broker: {meta_trader_5.last_error()}")
        else:
            click.echo(f"Connected to MT5 installation: {mt5_to_connect.path}")
            SingletonService().put(S.CONNECTED_MT5, mt5_to_connect)
            if term_info.connected:

                mt5_to_connect.trade_allowed = term_info.trade_allowed
                mt5_to_connect.tradeapi_disabled = term_info.tradeapi_disabled
                mt5_to_connect.notifications_enabled = term_info.notifications_enabled
                mt5_to_connect.mqid = term_info.mqid
                databaseService.updateMetatrader(mt5_to_connect)
                click.echo(f"Updated MT5 permissions info")

                version_info: Optional[tuple[int, int, str]] = meta_trader_5.version()
                mt5_to_connect.terminal_version = f"{version_info[0]}.{version_info[1]} {version_info[2]}"
                mt5_to_connect.build = version_info[1]
                mt5_to_connect.release_date = version_info[2]
                databaseService.updateMetatrader(mt5_to_connect)
                click.echo(f"Updated MT5 version info")
    else:
        click.echo("Invalid choice. No MT5 installation connected.")

@click.command()
def disconnect_mt5():
    """ Disconnect from a MetaTrader 5 installation"""
    connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
    if connected_mt5 is not None:
        """Disconnect from the MetaTrader 5 terminal."""
        try:
            if meta_trader_5.shutdown():
                print("[OK] Disconnected from MetaTrader 5")
            else:
                print(f"[WARN] meta_trader_5.shutdown() failed: {meta_trader_5.last_error()}")
        except Exception as e:
            print(f"[Error] During shutdown: {e}")
            
        mt5_pid = SingletonService().get(S.MT5_PID)
        if mt5_pid is not None:
            try:
                proc = psutil.Process(mt5_pid)
                proc.terminate()          # sends SIGTERM (graceful)
                proc.wait(timeout=5)      # wait up to 5 s for clean exit
                print(f"MT5 (PID {mt5_pid}) terminated gracefully")
            except psutil.TimeoutExpired:
                proc.kill()               # force-kill if it didn't exit in time
                print(f"MT5 (PID {mt5_pid}) force-killed")
            except psutil.NoSuchProcess:
                print("MT5 process already gone")
            except psutil.AccessDenied as e:
                print(f"Access denied killing PID {mt5_pid}: {e}")
            finally:        
                SingletonService().put(S.MT5_PID, None) # Clear the stored PID

        SingletonService().put(S.CONNECTED_MT5, None)
        click.echo(f"Disconnected from MT5 installation: {connected_mt5.path}")
    else:
        click.echo("No MT5 installation is currently connected.")

MT5_SUB_COMMANDS: list[tuple[str, str | None, Callable[[], str], str | None]] = [
    ['Append a MT5', append_mt5.callback.__name__.replace("_", "-"), explain_empty, None], 
    ['List all MT5', list_mt5.callback.__name__.replace("_", "-"), explain_empty, None], 
    ['Connect to a MT5', connect_mt5.callback.__name__.replace("_", "-"), explain_empty, None],
    ['Update a MT5', update_mt5.callback.__name__.replace("_", "-"), explain_empty, None],
    ['Disconnect from a MT5', disconnect_mt5.callback.__name__.replace("_", "-"), explain_empty, None],
    ['Delete a MT5', delete_mt5.callback.__name__.replace("_", "-"), explain_empty, None],
    ['Return to previous menu', None, explain_empty, None]
]

@click.group()
@click.pass_context
def metatrader5(ctx):
    """ Load the configuration from the XML file.  """
    global databaseService
    databaseService = SingletonService().get(S.DATABASE_SERVICE)

    choice = None
    while True:
        mt5_installations: list[MetatraderConfig] = databaseService.listMetatraders()
        click.echo(empty_string)
        click.echo("MT5 Installations:")
        if bool(mt5_installations) and len(mt5_installations) > 0:
            for mt5 in mt5_installations:
                click.echo(f"- {mt5}")
        else:
            click.echo("No MT5 installations found.")
        click.echo(empty_string)

        connected_mt5: MetatraderConfig | None = SingletonService().get(S.CONNECTED_MT5)
        if bool(connected_mt5):
            click.echo(f"Currently connected to MT5 installation: {connected_mt5.path}")
        else:
            click.echo("Not connected to any MT5 installation.")

        result = None
        if choice is None:
            choice = interactive_menu(MT5_SUB_COMMANDS)
        
        if bool(choice)and bool(choice[1]):
            click.echo(f"Invoking command: {choice}")
            ctx.invoke(ctx.command.commands[choice[1]])
            result = choice[3]
            choice = None  # Reset choice to None after invoking the command
        else:
            click.echo("metatrader5.py: Back to the previous menu")
            return result

metatrader5.add_command(append_mt5)
metatrader5.add_command(list_mt5)
metatrader5.add_command(connect_mt5)
metatrader5.add_command(update_mt5)
metatrader5.add_command(disconnect_mt5)
metatrader5.add_command(delete_mt5)
