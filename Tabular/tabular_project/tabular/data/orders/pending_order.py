from tabular.data.base.base import Base
from sqlalchemy import Boolean, Column, Integer, Float, ForeignKey, String
from tabular.util.util.price_util import fmt_price


class PendingOrder(Base):
    __tablename__ = "PENDING_ORDER"

    id: int = Column("id", Integer, primary_key=True)
    account_id: int = Column("account_id", Integer, ForeignKey("ACCOUNT_CONFIG.id"), nullable=False)

    symbol_id:  int = Column("symbol_id", Integer, ForeignKey("SYMBOL_INFORMATION.id"), nullable=False)
    symbol: str = Column("symbol", String, nullable=False)

    generic_id:  int = Column("generic_id", Integer, ForeignKey("GENERIC_ORDER.id"), nullable=False)

    ticket: int = Column("ticket", Integer, nullable=False)
    magic: int = Column("magic", Integer, nullable=True)
    comment: str = Column("comment", String, nullable=True)
    external_id: str = Column("external_id", String, nullable=True)

    type_order: int = Column("type_order", Integer, nullable=False)
    type_time: int = Column("type_time", Integer, nullable=False)
    type_filling: int = Column("type_filling", Integer, nullable=False)
    digits: int = Column("digits", Integer, nullable=False)
    
    volume: float = Column("volume", Float, nullable=False)
    entry: float = Column("entry", Float, nullable=False)
    sl: float = Column("sl", Float, nullable=False)
    tp: float = Column("tp", Float, nullable=False)

    def __init__(self):
        pass

    def __repr__(self):
        return f"<PendingOrder(id={self.id}, account_id='{self.account_id}', symbol_id='{self.symbol_id}', ticket='{self.ticket}', volume='{self.volume}', digits'={self.digits}', entry='{fmt_price(self.entry, self.digits)}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}', magic='{self.magic}', comment='{self.comment}', external_id='{self.external_id}', type_order='{self.type_order}', type_time='{self.type_time}, type_filling='{self.type_filling}')>"
    
    def __str__(self):
        return f"<PO(ticket='{self.ticket}' symbol_id='{self.symbol_id}', volume='{self.volume}', digits'={self.digits}', entry='{fmt_price(self.entry, self.digits)}', sl='{fmt_price(self.sl, self.digits)}', tp='{fmt_price(self.tp, self.digits)}' )>"
    
    


