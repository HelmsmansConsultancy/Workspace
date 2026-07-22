from tabular.data.base import Base
from typing import Optional
from sqlalchemy import Integer, Float, ForeignKey, String
from tabular.data.orders.specific_pending_order import SpecificPendingOrder
from tabular.util.util.price_util import fmt_price
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class GenericPendingOrder(Base):
    __tablename__ = "GEN_PEND_ORD"

    id: Mapped[int] = mapped_column("id", primary_key=True)

    specificPendingOrder: Mapped[SpecificPendingOrder] = relationship()
    
    symbol_id:  Mapped[int] = mapped_column("symbol_id", ForeignKey("GEN_SYMBOL_INFO.id"))
    symbol: Mapped[str] = mapped_column("symbol")

    magic: Mapped[Optional[int]] = mapped_column("magic")
    comment: Mapped[Optional[str]] = mapped_column("comment")
    external_id: Mapped[Optional[str]] = mapped_column("external_id")

    type_order: Mapped[int] = mapped_column("type_order")
    type_time: Mapped[int] = mapped_column("type_time")
    type_filling: Mapped[int] = mapped_column("type_filling")
    digits: Mapped[int] = mapped_column("digits")

    volume: Mapped[float] = mapped_column("volume")
    entry: Mapped[float] = mapped_column("entry")
    sl: Mapped[float] = mapped_column("sl")
    tp: Mapped[float] = mapped_column("tp")

    def __init__(self):
        pass

    def __repr__(self):
        return f"<GenericPendingOrder(id={self.id}, symbol='{self.symbol}', symbol_id='{self.symbol_id}', volume='{fmt_price(self.volume, 2)}', digits={self.digits}, entry='{fmt_price(self.entry, self.digits)}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}', magic='{self.magic}', comment='{self.comment}', external_id='{self.external_id}', type_order='{self.type_order}', type_time='{self.type_time}, type_filling='{self.type_filling}')>"
    
    def __str__(self):
        return f"<GOP(symbol='{self.symbol}', volume='{fmt_price(self.volume, 2)}', entry='{fmt_price(self.entry, self.digits)}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}' )>"
    
    def isBuy(self) -> bool:
        return self.tp > self.sl
    


