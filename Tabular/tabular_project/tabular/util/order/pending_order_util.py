from tabular.data.orders.specific_pending_order import SpecificPendingOrder
from MetaTrader5 import TradeOrder
from types import SimpleNamespace

def copyValuesIntoPendingOrder(tradeOrder: TradeOrder, spo: SpecificPendingOrder):
    d = SimpleNamespace(**tradeOrder._asdict())
    spo.ticket=d.ticket
    spo.magic=d.magic
    spo.type_order=d.type
    spo.type_time=d.type_time
    spo.type_filling=d.type_filling
    # pendingOrder.digits=d.digits There are no digits in tradeorder
    spo.entry=d.price_open
    spo.sl=d.sl
    spo.tp=d.tp
    spo.volume=d.volume_current
    spo.comment=d.comment
    spo.external_id=d.external_id