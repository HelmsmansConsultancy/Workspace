from tabular.data.base import Base
from sqlalchemy import Boolean, Column, Integer, Float, ForeignKey, String
from decimal import Decimal


class OpenPosition(Base):
    __tablename__ = "OPEN_POSITION"

    id: int = Column("id", Integer, primary_key=True)
    account_id: int = Column("account_id", Integer, ForeignKey("ACCOUNT_CONFIG.id"), nullable=False)

    ticket: int = Column("ticket", Integer, nullable=False)
    magic: int = Column("magic", Integer, nullable=True)
    comment: str = Column("comment", String, nullable=True)
    external_id: str = Column("external_id", String, nullable=True)

    type_order: int = Column("type_order", Integer, nullable=False)
    profit: float = Column("profit", Float, nullable=False)
    swap: float = Column("swap", Float, nullable=False)

    volume: float = Column("volume", Float, nullable=False)
    entry: float = Column("entry", Float, nullable=False)
    sl: float = Column("sl", Float, nullable=False)
    tp: float = Column("tp", Float, nullable=False)
    symbol: str = Column("symbol", String, nullable=False)

    def __init__(self):
        pass

    def __repr__(self):
        return f"<PendingOrder(id={self.id}, account_id='{self.account_id}', symbol='{self.symbol}', ticket='{self.ticket}', volume='{self.volume}', entry='{self.entry}', sl='{self.sl}', tp='{self.tp}', magic='{self.magic}', comment='{self.comment}', external_id='{self.external_id}', type_order='{self.type_order}', profit='{self.profit}, swap='{self.swap}')>"
    
    def __str__(self):
        return f"<PO(ticket='{self.ticket}' symbol='{self.symbol}', volume='{self.volume}', profit='{self.profit}', sl='{self.sl}', tp='{self.tp}' )>"
    
    


