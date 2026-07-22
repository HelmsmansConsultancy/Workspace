from tabular.data.base.base import Base
from sqlalchemy import Boolean, Column, Integer, Float, ForeignKey, String
from tabular.util.util.price_util import fmt_price
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class SpecificPendingOrder(Base):
    __tablename__ = "SPECIFIC_PENDING_ORDER"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    account_id: Mapped[int] = mapped_column("account_id", ForeignKey("ACCOUNT_CONFIG.id"), nullable=False)

    symbol_id:  Mapped[int] = mapped_column("symbol_id", ForeignKey("SYMBOL_INFORMATION.id"), nullable=False)
    symbol: Mapped[str] = mapped_column("symbol", nullable=False)

    generic_id:  Mapped[int] = mapped_column("generic_id", ForeignKey("GENERIC_PENDING_ORDER.id"), nullable=False)

    ticket: Mapped[int] = mapped_column("ticket", nullable=False)
    magic: Mapped[int] = mapped_column("magic", nullable=True)
    comment: Mapped[str] = mapped_column("comment", nullable=True)
    external_id: Mapped[str] = mapped_column("external_id", nullable=True)

    type_order: Mapped[int] = mapped_column("type_order", nullable=False)
    type_time: Mapped[int] = mapped_column("type_time", nullable=False)
    type_filling: Mapped[int] = mapped_column("type_filling", nullable=False)
    digits: Mapped[int] = mapped_column("digits", nullable=False)
    
    volume: Mapped[float] = mapped_column("volume", nullable=False)
    entry: Mapped[float] = mapped_column("entry", nullable=False)
    sl: Mapped[float] = mapped_column("sl", nullable=False)
    tp: Mapped[float] = mapped_column("tp", nullable=False)

    def __init__(self):
        pass

    def __repr__(self):
        return f"<SpecificPendingOrder(id={self.id}, account_id='{self.account_id}', symbol='{self.symbol}', symbol_id='{self.symbol_id}', ticket='{self.ticket}', volume='{fmt_price(self.volune, 2)}', digits'={self.digits}', entry='{fmt_price(self.entry, self.digits)}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}', magic='{self.magic}', comment='{self.comment}', external_id='{self.external_id}', type_order='{self.type_order}', type_time='{self.type_time}, type_filling='{self.type_filling}')>"
    
    def __str__(self):
        return f"<SPO(ticket='{self.ticket}'symbol='{self.symbol}', volume='{fmt_price(self.volume, 2)}', digits'={self.digits}', entry='{fmt_price(self.entry, self.digits)}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}' )>"
    
    


