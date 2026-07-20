from tabular.data.base import Base
from sqlalchemy import Boolean, Column, Integer, Numeric, ForeignKey, String, Float



class SymbolInfomation(Base):
    __tablename__ = "SYMBOL_INFORMATION"

    id: int = Column("id", Integer, primary_key=True)
    account_id: int = Column("account_id", Integer, ForeignKey("ACCOUNT_CONFIG.id"), nullable=False)
    name: str = Column("name",String, nullable=False)
    symbol: str = Column("symbol",String, nullable=False)
    digits: int = Column("digits", Integer, nullable=False)
    spread: int = Column("spread", Integer, nullable=False)
    select: bool = Column("select", Boolean, nullable=False)
    point: float = Column("point", Float, nullable=False)

    def __init__(self, account_id: int):
        self.account_id = account_id

    def __repr__(self):
        return f"<SymbolInfomation(id={self.id}, account_id={self.account_id}, symbol={self.symbol} name={self.name} digits={self.digits}, spread={self.spread}, select={self.select}, point={self.point})>"
        
    
    def __str__(self):
        return f"<SymbolInfomation(id={self.id} name={self.name}, digits={self.digits},  point={self.point}, symbol={self.symbol})>"



