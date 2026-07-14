from tabular.data.symbols.symbol_info import SymbolInfomation
from MetaTrader5 import SymbolInfo
from types import SimpleNamespace

def copyValuesInto(symbolInfo: SymbolInfo, symbol: SymbolInfomation):
    s = SimpleNamespace(symbolInfo._asdict())
    symbol.name=s.name
    symbol.pair = getPairFromName(s.name)
    symbol.digits=s.digits
    symbol.spread=s.spread
    symbol.select=s.select
    symbol.point=s.point
    
def getPairFromName(name: str) -> str:
    match name:
        case val if "AUDCAD" in val:
            return "AUDCAD"
        case val if "AUDCHF" in val:
            return "AUDCHF"
        case val if "AUDJPY" in val:
            return "AUDJPY"
        case val if "AUDNZD" in val:
            return "AUDNZD"
        case val if "AUDUSD" in val:
            return "AUDUSD"
        case val if "CADCHF" in val:
            return "CADCHF"
        case val if "CADJPY" in val:
            return "CADJPY"
        case val if "EURAUD" in val:
            return "EURAUD"
        case val if "EURCAD" in val:
            return "EURCAD"
        case val if "EURCHF" in val:
            return "EURCHF"
        case val if "EURGBP" in val:
            return "EURGBP"
        case val if "EURJPY" in val:
            return "EURJPY"
        case val if "EURNZD" in val:
            return "EURNZD"
        case val if "EURUSD" in val:
            return "EURUSD"
        case val if "GBPCAD" in val:
            return "GBPCAD"
        case val if "GBPCHF" in val:
            return "GBPCHF"
        case val if "GBPJPY" in val:
            return "GBPJPY"
        case val if "GBPNZD" in val:
            return "GBPNZD"
        case val if "GBPUSD" in val:
            return "GBPUSD"
        case val if "NZDCAD" in val:
            return "NZDCAD"
        case val if "NZDCHF" in val:
            return "NZDCHF"
        case val if "NZDJPY" in val:
            return "NZDJPY"
        case val if "NZDUSD" in val:
            return "NZDUSD"
        case val if "USDCAD" in val:
            return "USDCAD"
        case val if "USDCHF" in val:
            return "USDCHF"
        case val if "USDJPY" in val:
            return "USDJPY"
        case _:
            return name
