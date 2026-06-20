
import MetaTrader5 as mt5
from rich.console import Console

console = Console()

class Mt5Service():
    
    def __init__(self):
        pass

    def connect(self, path_to_executable):
        console.print("Connect" + path_to_executable)
        if not mt5.initialize(path_to_executable):
            print("initialize() failed, error code =", mt5.last_error())
            mt5.shutdown()
        else:
            console.print(mt5.account_info())  # Print account information
            positions = mt5.positions_get()
            if positions is None:
                print("No positions, error code =", mt5.last_error())
            else:
                for pos in positions:
                    print(pos._asdict())
            mt5.shutdown()


        