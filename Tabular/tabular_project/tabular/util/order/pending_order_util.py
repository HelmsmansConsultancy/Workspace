from tabular.data.pending_order import PendingOrder
from MetaTrader5 import TradeOrder
from types import SimpleNamespace

def copyValuesInto(tradeOrder: TradeOrder, pendingOrder: PendingOrder):
    d = SimpleNamespace(**tradeOrder._asdict())
    pendingOrder.ticket=d.ticket
    pendingOrder.magic=d.magic
    pendingOrder.type_order=d.type
    pendingOrder.type_time=d.type_time
    pendingOrder.type_filling=d.type_filling
    pendingOrder.symbol=d.symbol
    pendingOrder.entry=d.price_open
    pendingOrder.sl=d.sl
    pendingOrder.tp=d.tp
    pendingOrder.volume=d.volume_current
    pendingOrder.comment=d.comment
    pendingOrder.external_id=d.external_id