from typing import Final
from decimal import Decimal

class S:
    ACCOUNTS: Final = "accounts"
    APPLICATION_CONFIG: Final = "ApplicationConfig"
    CENT: Final = Decimal("0.01")
    CONNECTED_ACCOUNT: Final = "connected_account" 
    CONNECTED_MT5: Final = "connected_mt5" 
    DATABASE_SERVICE: Final = "DatabaseService"
    MENU_SERVICE: Final = "MenuService"
    METATRADER5_SERVICE: Final = "Metatrader5Service"
    METATRADERS: Final = "Metatraders"
    MT5_PID: Final = "mt5_pid"
    START_DIR: Final = "start_dir"

    def __init__(self):
        pass