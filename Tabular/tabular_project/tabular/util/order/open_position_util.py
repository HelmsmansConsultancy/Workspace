from tabular.data.open_position import OpenPosition
from MetaTrader5 import TradePosition
from types import SimpleNamespace
from tabular.util.symbols_util import getPairFromName

def copyValuesInto(tradePosition: TradePosition, openPosition: OpenPosition):
    d = SimpleNamespace(**tradePosition._asdict())
    openPosition.ticket=d.ticket
    openPosition.magic=d.magic
    openPosition.type_order=d.type
    openPosition.profit=d.profit
    openPosition.swap=d.swap
    openPosition.pair=getPairFromName(d.symbol) 
    openPosition.symbol=d.symbol
    openPosition.entry=d.price_open
    openPosition.sl=d.sl
    openPosition.tp=d.tp
    openPosition.volume=d.volume
    openPosition.comment=d.comment
    openPosition.external_id=d.external_id