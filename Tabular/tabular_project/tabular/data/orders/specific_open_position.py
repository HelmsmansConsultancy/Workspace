from tabular.data.base import Base
from typing import Optional
from sqlalchemy import ForeignKey
from tabular.util.util.price_util import fmt_price
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class SpecificOpenPosition(Base):
    __tablename__ = "SPEC_OPEN_POS"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    account_id: Mapped[int] = mapped_column("account_id", ForeignKey("ACC_CONF.id"))
    
    symbol_id:  Mapped[int] = mapped_column("symbol_id", ForeignKey("SPEC_SYMBOL_INFO.id"))
    symbol: Mapped[str] = mapped_column("symbol")

    generic_id:  Mapped[int] = mapped_column("generic_id", ForeignKey("GEN_OPEN_POS.id"))

    ticket: Mapped[int] = mapped_column("ticket")
    magic: Mapped[Optional[int]] = mapped_column("magic")
    comment: Mapped[Optional[str]] = mapped_column("comment")
    external_id: Mapped[Optional[str]] = mapped_column("external_id")

    type_order: Mapped[int] = mapped_column("type_order")
    profit: Mapped[float] = mapped_column("profit")
    swap: Mapped[float] = mapped_column("swap")
    digits: Mapped[int] = mapped_column("digits")

    volume: Mapped[float] = mapped_column("volume")
    entry: Mapped[float] = mapped_column("entry")
    sl: Mapped[float] = mapped_column("sl")
    tp: Mapped[float] = mapped_column("tp")

    def __init__(self):
        pass

    def __repr__(self):
        return f"<SpecificOpenPosition(id={self.id}, account_id='{self.account_id}', symbol_id='{self.symbol_id}', ticket='{self.ticket}', volume='{self.volume}', digits'={self.digits}', entry='{fmt_price(self.entry, self.digits)}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}', magic='{self.magic}', comment='{self.comment}', external_id='{self.external_id}', type_order='{self.type_order}', profit='{self.profit}, swap='{self.swap}')>"
    
    def __str__(self):
        return f"<SOP(ticket='{self.ticket}' symbol_id='{self.symbol_id}', volume='{self.volume}', profit='{self.profit}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}')>"
    
    


