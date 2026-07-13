from tabular.data.symbol_info import SymbolInfomation
from MetaTrader5 import SymbolInfo
from types import SimpleNamespace

def copyValuesInto(symbolInfo: SymbolInfo, symbol: SymbolInfomation):
    s = SimpleNamespace(symbolInfo._asdict())
    symbol.name=s.name
    symbol.digits=s.digits
    symbol.spread=s.spread
    symbol.select=s.select
    symbol.point=s.point