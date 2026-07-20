from tabular.data.base.base import Base
from sqlalchemy import Boolean, Column, Integer, Float, ForeignKey, String
from decimal import Decimal
from tabular.util.util.price_util import fmt_price

class GenericPosition(Base):
    __tablename__ = "GENERIC_POSITION"

    id: int = Column("id", Integer, primary_key=True)

    symbol_id:  int = Column("symbol_id", Integer, ForeignKey("SYMBOL_INFORMATION.id"), nullable=False)
    symbol: str = Column("symbol", String, nullable=False)

    ticket: int = Column("ticket", Integer, nullable=False)
    magic: int = Column("magic", Integer, nullable=True)
    comment: str = Column("comment", String, nullable=True)
    external_id: str = Column("external_id", String, nullable=True)

    type_order: int = Column("type_order", Integer, nullable=False)
    profit: float = Column("profit", Float, nullable=False)
    swap: float = Column("swap", Float, nullable=False)
    digits: int = Column("digits", Integer, nullable=False)

    volume: float = Column("volume", Float, nullable=False)
    entry: float = Column("entry", Float, nullable=False)
    sl: float = Column("sl", Float, nullable=False)
    tp: float = Column("tp", Float, nullable=False)

    def __init__(self):
        pass

    def __repr__(self):
        return f"<PendingOrder(id={self.id}, symbol_id='{self.symbol_id}', symbol='{self.symbol}', ticket='{self.ticket}', volume='{self.volume}', digits'={self.digits}' ,entry='{fmt_price(self.entry, self.digits)}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}', magic='{self.magic}', comment='{self.comment}', external_id='{self.external_id}', type_order='{self.type_order}', profit='{self.profit}, swap='{self.swap}')>"
    
    def __str__(self):
        digits = 5
        return f"<PO(ticket='{self.ticket}' symbol_id='{self.symbol_id}', volume='{self.volume}', profit='{self.profit}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}' )>"
    
    


