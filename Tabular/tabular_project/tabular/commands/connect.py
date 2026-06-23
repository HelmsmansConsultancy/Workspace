import click
import MetaTrader5 as mt5
import psutil
import subprocess
from rich.console import Console
from ..service.singleton_service import SingletonService
from ..data.account_config import AccountConfig
from ..util.fileutils import list_files

console = Console()

def disconnect():
    """Disconnect from the MetaTrader 5 terminal."""
    try:
        if mt5.shutdown():
            print("[OK] Disconnected from MetaTrader 5")
        else:
            print(f"[WARN] mt5.shutdown() failed: {mt5.last_error()}")
    except Exception as e:
        print(f"[Error] During shutdown: {e}")
    
    mt5_pid = SingletonService().get("mt5_pid")
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
           SingletonService().put("mt5_pid", None) # Clear the stored PID

def query_terminal_info():
    """Query terminal (platform) metadata."""
    print("\n===== TERMINAL INFO =====")
    try:
        info = mt5.terminal_info()
        if info is None:
            print(f"  [WARN] terminal_info() returned None: {mt5.last_error()}")
            return
        for field, value in info._asdict().items():
            print(f"  {field}: {value}")
    except AttributeError as e:
        print(f"  [AttributeError] {e}")
    except Exception as e:
        print(f"  [Error] terminal_info: {e}")


def query_version():
    """Query MT5 version tuple."""
    print("\n===== VERSION =====")
    try:
        version = mt5.version()
        if version is None:
            print(f"  [WARN] version() returned None: {mt5.last_error()}")
            return
        print(f"  Build: {version[0]}  Date: {version[1]}  Time: {version[2]}")
    except Exception as e:
        print(f"  [Error] version: {e}")


def query_account_info():
    """Query trading account details."""
    print("\n===== ACCOUNT INFO =====")
    try:
        info = mt5.account_info()
        if info is None:
            print(f"  [WARN] account_info() returned None: {mt5.last_error()}")
            return
        for field, value in info._asdict().items():
            print(f"  {field}: {value}")
    except AttributeError as e:
        print(f"  [AttributeError] {e}")
    except Exception as e:
        print(f"  [Error] account_info: {e}")


def query_symbols():
    """Query all available symbols and their properties."""
    print("\n===== SYMBOLS =====")
    try:
        symbols = mt5.symbols_get()
        if symbols is None:
            print(f"  [WARN] symbols_get() returned None: {mt5.last_error()}")
            return []
        print(f"  Total symbols: {len(symbols)}")
        symbol_names = []
        for s in symbols:
            try:
                d = s._asdict()
                symbol_names.append(d["name"])
                print(f"  [{d['name']}]  path={d.get('path','')}  "
                      f"digits={d.get('digits','')}  "
                      f"spread={d.get('spread','')}  "
                      f"trade_mode={d.get('trade_mode','')}")
            except AttributeError:
                print(f"  [WARN] Unexpected symbol format: {s}")
        return symbol_names
    except TypeError as e:
        print(f"  [TypeError] symbols_get: {e}")
        return []
    except Exception as e:
        print(f"  [Error] symbols_get: {e}")
        return []


def query_symbol_info(symbol: str):
    """Query detailed info for a single symbol."""
    print(f"\n  -- Symbol info: {symbol} --")
    try:
        info = mt5.symbol_info(symbol)
        if info is None:
            print(f"    [WARN] symbol_info({symbol}) returned None: {mt5.last_error()}")
            return
        for field, value in info._asdict().items():
            print(f"    {field}: {value}")
    except AttributeError as e:
        print(f"    [AttributeError] {e}")
    except Exception as e:
        print(f"    [Error] symbol_info({symbol}): {e}")


def query_symbol_tick(symbol: str):
    """Query the latest tick for a symbol."""
    print(f"\n  -- Latest tick: {symbol} --")
    try:
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            print(f"    [WARN] No tick for {symbol}: {mt5.last_error()}")
            return
        d = tick._asdict()
        print(f"    bid={d.get('bid')}  ask={d.get('ask')}  "
              f"last={d.get('last')}  volume={d.get('volume')}  "
              f"time={datetime.fromtimestamp(d.get('time', 0))}")
    except AttributeError as e:
        print(f"    [AttributeError] {e}")
    except Exception as e:
        print(f"    [Error] symbol_info_tick({symbol}): {e}")


def query_market_book(symbol: str):
    """Query order book (Market Depth) for a symbol."""
    print(f"\n  -- Market book: {symbol} --")
    try:
        if not mt5.market_book_add(symbol):
            print(f"    [WARN] market_book_add({symbol}) failed: {mt5.last_error()}")
            return
        time.sleep(0.2)
        book = mt5.market_book_get(symbol)
        if book is None:
            print(f"    [WARN] market_book_get({symbol}) returned None: {mt5.last_error()}")
        else:
            for item in book:
                print(f"    {item}")
        mt5.market_book_release(symbol)
    except Exception as e:
        print(f"    [Error] market_book({symbol}): {e}")


def query_orders():
    """Query all open orders."""
    print("\n===== OPEN ORDERS =====")
    try:
        orders = mt5.orders_get()
        if orders is None:
            print(f"  [WARN] orders_get() returned None: {mt5.last_error()}")
            return
        print(f"  Open orders: {len(orders)}")
        for o in orders:
            print(f"  {o}")
    except TypeError as e:
        print(f"  [TypeError] orders_get: {e}")
    except Exception as e:
        print(f"  [Error] orders_get: {e}")


def query_positions():
    """Query all open positions."""
    print("\n===== OPEN POSITIONS =====")
    try:
        positions = mt5.positions_get()
        if positions is None:
            print(f"  [WARN] positions_get() returned None: {mt5.last_error()}")
            return
        print(f"  Open positions: {len(positions)}")
        for p in positions:
            print(f"  {p}")
    except TypeError as e:
        print(f"  [TypeError] positions_get: {e}")
    except Exception as e:
        print(f"  [Error] positions_get: {e}")


def query_history_orders(from_date: datetime, to_date: datetime):
    """Query historical orders within a date range."""
    print("\n===== HISTORY ORDERS =====")
    try:
        orders = mt5.history_orders_get(from_date, to_date)
        if orders is None:
            print(f"  [WARN] history_orders_get() returned None: {mt5.last_error()}")
            return
        print(f"  Historical orders: {len(orders)}")
        for o in orders[:10]:   # print first 10 to avoid flooding console
            print(f"  {o}")
        if len(orders) > 10:
            print(f"  ... and {len(orders) - 10} more.")
    except TypeError as e:
        print(f"  [TypeError] history_orders_get: {e}")
    except ValueError as e:
        print(f"  [ValueError] history_orders_get: {e}")
    except Exception as e:
        print(f"  [Error] history_orders_get: {e}")


def query_history_deals(from_date: datetime, to_date: datetime):
    """Query historical deals within a date range."""
    print("\n===== HISTORY DEALS =====")
    try:
        deals = mt5.history_deals_get(from_date, to_date)
        if deals is None:
            print(f"  [WARN] history_deals_get() returned None: {mt5.last_error()}")
            return
        print(f"  Historical deals: {len(deals)}")
        for d in deals[:10]:
            print(f"  {d}")
        if len(deals) > 10:
            print(f"  ... and {len(deals) - 10} more.")
    except TypeError as e:
        print(f"  [TypeError] history_deals_get: {e}")
    except ValueError as e:
        print(f"  [ValueError] history_deals_get: {e}")
    except Exception as e:
        print(f"  [Error] history_deals_get: {e}")


def query_rates(symbol: str, timeframe=mt5.TIMEFRAME_H1, count: int = 100):
    """Query OHLCV bars for a symbol."""
    print(f"\n  -- Rates ({symbol}, H1, last {count} bars) --")
    try:
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None:
            print(f"    [WARN] copy_rates_from_pos returned None: {mt5.last_error()}")
            return
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        print(df.tail(5).to_string(index=False))
    except ImportError:
        print("    [ImportError] pandas not installed; printing raw data instead.")
        for r in rates[-5:]:
            print(f"    {r}")
    except TypeError as e:
        print(f"    [TypeError] copy_rates_from_pos: {e}")
    except Exception as e:
        print(f"    [Error] copy_rates_from_pos({symbol}): {e}")


def query_ticks_range(symbol: str, from_date: datetime, to_date: datetime):
    """Query raw ticks for a symbol over a short range."""
    print(f"\n  -- Ticks range: {symbol} --")
    try:
        ticks = mt5.copy_ticks_range(symbol, from_date, to_date, mt5.COPY_TICKS_ALL)
        if ticks is None:
            print(f"    [WARN] copy_ticks_range returned None: {mt5.last_error()}")
            return
        print(f"    Ticks fetched: {len(ticks)}")
        for t in ticks[:3]:
            print(f"    {t}")
    except TypeError as e:
        print(f"    [TypeError] copy_ticks_range: {e}")
    except Exception as e:
        print(f"    [Error] copy_ticks_range({symbol}): {e}")

def initialize_connection(path: str) -> bool:
    """Initialize and return True if the MT5 terminal connects successfully."""
    # Snapshot PIDs before initialization
    before = {p.pid for p in psutil.process_iter(["pid", "name"])
              if p.info["name"] == "terminal64.exe"}

    try:
        if not mt5.initialize(path=path):
            error = mt5.last_error()
            print(f"[ERROR] mt5.initialize() failed: {error}")
            return False
    except ConnectionError as e:
        print(f"[ConnectionError] {e}")
        return False
    except FileNotFoundError as e:
        print(f"[FileNotFoundError] Terminal executable not found: {e}")
        return False
    except PermissionError as e:
        print(f"[PermissionError] Cannot access terminal: {e}")
        return False
    except OSError as e:
        print(f"[OSError] OS-level error during initialization: {e}")
        return False
    except Exception as e:
        print(f"[UnexpectedError] During initialization: {e}")
        return False
    
    # Snapshot PIDs before initialization
    after = {p.pid for p in psutil.process_iter(["pid", "name"])
              if p.info["name"] == "terminal64.exe"}

    new_pids = after - before
    if new_pids:
        mt5_pid = new_pids.pop()
        print(f"MT5 started with PID {mt5_pid}")
        SingletonService().put("mt5_pid", mt5_pid)
    else:
        print("MT5 was already running; PID not tracked")

def interactive_menu(accounts: list[AccountConfig]) -> AccountConfig:
    click.echo("Choose which account...")
    for i, account in enumerate(accounts, 1):
        click.echo(f"  {i}. {account.id}")
    idx = click.prompt(
        "Enter number",
        type=click.IntRange(1, len(accounts))
    )
    return idx - 1

@click.command()
def connect():
    accounts: list[AccountConfig] = SingletonService().get("accounts")
    idx = 0
    """Connect to a data source."""        
    if len(accounts) == 0:
        click.echo("No accounts found in the configuration.")
        return
    if len(accounts) == 0:
        idx = interactive_menu(accounts)

    account = accounts[idx]
    click.echo(f"Connecting to: {account.backend.firm} {account.id} {account.path} of type {account.type} with Size {account.money.base} {account.money.currency}")

    initialize_connection(account.path)
    #query_terminal_info()
    #query_version()
    #query_account_info()
    #query_symbols()
    #query_orders()
    #query_positions()
    #query_history_orders()
    #query_history_deals()
    #query_rates()
    #query_ticks_range()




