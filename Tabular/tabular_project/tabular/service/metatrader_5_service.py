import psutil
import MetaTrader5 as meta_trader_5
from tabular.data.settings.metatrader_config import MetatraderConfig
from tabular.data.settings.account_config import AccountConfig
from tabular.service.singleton_service import SingletonService
from tabular.service.s import S
from rich.console import Console
from MetaTrader5 import AccountInfo, TerminalInfo, TradeOrder, TradePosition, SymbolInfo
from tabular.data.orders.generic_pending_order import GenericPendingOrder
from tabular.util.util.price_util import to_decimal

console = Console()

class Metatrader5Service():
    path: str

    def __init__(self):
        self.console = Console()

    def getAccountInfo(self) -> AccountInfo: 
        account_info: AccountInfo = meta_trader_5.account_info()
        return account_info

    def login(self, account_login: int, password: str, server: str) -> AccountInfo:
        result: bool = meta_trader_5.login(account_login, password=password, server=server, timeout=60000)
        if bool(result):
            return meta_trader_5.account_info()
        else:
            return None

    def deletePendingOrder(self, ticket : int) -> None:
        request = {
            "action": meta_trader_5.TRADE_ACTION_REMOVE,
            "order":  ticket,   # int: the pending order's ticket
        }

        result = meta_trader_5.order_send(request)
        
        if result.retcode != meta_trader_5.TRADE_RETCODE_DONE:
            print(f"Delete failed: retcode={result.retcode}, comment={result.comment}")
        else:
            print(f"Order {ticket} removed.")

    def placePendingOrder(self, spo: GenericPendingOrder) -> TradeOrder:
        if not meta_trader_5.symbol_select(spo.symbol, True):
            return None
        
        request = {
            "action": meta_trader_5.TRADE_ACTION_PENDING,
            "symbol": spo.symbol,
            "volume": float(to_decimal(spo.volume, 2)),
            "type": meta_trader_5.ORDER_TYPE_BUY_LIMIT if spo.isBuy() else meta_trader_5.ORDER_TYPE_SELL_LIMIT, 
            "price": float(to_decimal(spo.entry, spo.digits)),
            "sl": float(to_decimal(spo.sl, spo.digits)),
            "tp": float(to_decimal(spo.tp, spo.digits)), 
            "deviation": 0,
            "magic": spo.magic,                         
            "comment": spo.comment,
            "type_time": meta_trader_5.ORDER_TIME_GTC,        
            "type_filling": meta_trader_5.ORDER_FILLING_RETURN,
        }
        self.console.print(f"{request}")
        
        result = meta_trader_5.order_send(request)
        
        if result.retcode == meta_trader_5.TRADE_RETCODE_DONE:
            print(result)
            orders = meta_trader_5.orders_get(ticket=result.order)
            trade_order = orders[0] if orders else None
            return trade_order
        else:
            print(f"Order failed, retcode={result.retcode}")
            return

    def getSymbolInfo(self, accountId: int) -> list[SymbolInfo]:
        # get the SymbolInfo
        connected_account: AccountConfig = SingletonService().get(S.CONNECTED_ACCOUNT)
        if accountId != connected_account.id:
            raise ValueError(f"AccountId={accountId} != connected_account.id=={connected_account.id}")
        symbolInfos: list[SymbolInfo] = meta_trader_5.symbols_get()
        # self.console.print(symbolInfos)
        return symbolInfos

    def getPendingOrders(self, accountId: int) -> list[TradeOrder]:
        # get the limig or stop orders
        connected_account: AccountConfig = SingletonService().get(S.CONNECTED_ACCOUNT)
        self.console.print(f"getPendingOrders() {accountId} - {connected_account}")
        if accountId != connected_account.id:
            raise ValueError(" accountId != connected_account.id")
        tradeOrders: list[TradeOrder] = meta_trader_5.orders_get()
        
        # if bool(tradeOrders):
        #     for tradeOrder in tradeOrders:
        #         self.console.print(tradeOrder)
        return tradeOrders

    def getTradeDeals(self, accountId: int) -> list[TradePosition ]:
        # get the limig or stop orders
        connected_account: AccountConfig = SingletonService().get(S.CONNECTED_ACCOUNT)
        if accountId != connected_account.id:
            raise ValueError(" accountId != connected_account.id")
        tradePositions: list[TradePosition] = meta_trader_5.positions_get()
        
        if bool(tradePositions):
            for tradePosition in tradePositions:
                self.console.print(tradePosition)
        return tradePositions

    def connect_mt5(self, mt5_to_connect: MetatraderConfig) -> MetatraderConfig:
        # Snapshot PIDs before initialization
        before = {p.pid for p in psutil.process_iter(["pid", "name"])
                if p.info["name"] == "terminal64.exe"}
        
        # Perform connection logic here
        meta_trader_5.initialize(path=mt5_to_connect.path)

        term_info: TerminalInfo | None = meta_trader_5.terminal_info()
        if term_info is None or not term_info.connected:
            raise ConnectionError(f"Failed to connect to MT5 installation at {mt5_to_connect.path}. Error: {meta_trader_5.last_error()}")
        else:
            SingletonService().put(S.CONNECTED_MT5, mt5_to_connect)

            if term_info.connected:
                if mt5_to_connect.trade_allowed is None or mt5_to_connect.tradeapi_disabled is None or mt5_to_connect.notifications_enabled is None or mt5_to_connect.mqid is None:
                    mt5_to_connect.trade_allowed = term_info.trade_allowed
                    mt5_to_connect.tradeapi_disabled = term_info.tradeapi_disabled
                    mt5_to_connect.notifications_enabled = term_info.notifications_enabled
                    mt5_to_connect.mqid = term_info.mqid
 #                   databaseService.updateMetatrader(mt5_to_connect)

                if mt5_to_connect.terminal_version is None or mt5_to_connect.build is None or mt5_to_connect.release_date is None:
                    version_info: Optional[tuple[int, int, str]] = meta_trader_5.version()
                    mt5_to_connect.terminal_version = f"{version_info[0]}.{version_info[1]} {version_info[2]}"
                    mt5_to_connect.build = version_info[1]
                    mt5_to_connect.release_date = version_info[2]
 #                   databaseService.updateMetatrader(mt5_to_connect)
        
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
        return mt5_to_connect
    
    def disconnect_mt5(self):
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