from tabular.data.orders.generic_pending_order import GenericPendingOrder
from MetaTrader5 import TradeOrder
from types import SimpleNamespace
from tabular.util.util.symbols_util import getSymbolFromName

def copyValuesIntoGenericOrder(tradeOrder: TradeOrder, genericOrder: GenericPendingOrder):
    d = SimpleNamespace(**tradeOrder._asdict())
    genericOrder.ticket=d.ticket
    genericOrder.magic=d.magic
    genericOrder.type_order=d.type
    genericOrder.type_time=d.type_time
    genericOrder.type_filling=d.type_filling
    # genericOrder.symbol=d.symbol

    # genericOrder.digits=d.digits No digits from TradeOrders
    genericOrder.entry=d.price_open
    genericOrder.sl=d.sl
    genericOrder.tp=d.tp
    genericOrder.volume=d.volume_current
    genericOrder.comment=d.comment
    genericOrder.external_id=d.external_id