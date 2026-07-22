from tabular.data.base.base import Base
from sqlalchemy import Column, Integer, Float, ForeignKey, String
from tabular.util.util.price_util import fmt_price
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class SpecificOpenPosition(Base):
    __tablename__ = "SPECIFIC_OPEN_POSITION"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    account_id: Mapped[int] = mapped_column("account_id", ForeignKey("ACCOUNT_CONFIG.id"), nullable=False)
    
    symbol_id:  Mapped[int] = mapped_column("symbol_id", ForeignKey("SYMBOL_INFORMATION.id"), nullable=False)
    symbol: Mapped[str] = mapped_column("symbol", nullable=False)

    generic_id:  Mapped[int] = mapped_column("generic_id", ForeignKey("GENERIC_OPEN_POSITION.id"), nullable=False)

    ticket: Mapped[int] = mapped_column("ticket", nullable=False)
    magic: Mapped[int] = mapped_column("magic", nullable=True)
    comment: Mapped[str] = mapped_column("comment", nullable=True)
    external_id: Mapped[str] = mapped_column("external_id", nullable=True)

    type_order: Mapped[int] = mapped_column("type_order", nullable=False)
    profit: Mapped[float] = mapped_column("profit", nullable=False)
    swap: Mapped[float] = mapped_column("swap", nullable=False)
    digits: Mapped[int] = mapped_column("digits", nullable=False)

    volume: Mapped[float] = mapped_column("volume", nullable=False)
    entry: Mapped[float] = mapped_column("entry", nullable=False)
    sl: Mapped[float] = mapped_column("sl", nullable=False)
    tp: Mapped[float] = mapped_column("tp", nullable=False)

    def __init__(self):
        pass

    def __repr__(self):
        return f"<SpecificOpenPosition(id={self.id}, account_id='{self.account_id}', symbol_id='{self.symbol_id}', ticket='{self.ticket}', volume='{self.volume}', digits'={self.digits}', entry='{fmt_price(self.entry, self.digits)}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}', magic='{self.magic}', comment='{self.comment}', external_id='{self.external_id}', type_order='{self.type_order}', profit='{self.profit}, swap='{self.swap}')>"
    
    def __str__(self):
        return f"<SOP(ticket='{self.ticket}' symbol_id='{self.symbol_id}', volume='{self.volume}', profit='{self.profit}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}')>"
    
    


