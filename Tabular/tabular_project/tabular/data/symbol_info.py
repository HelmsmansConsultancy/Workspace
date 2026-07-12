from tabular.data.base import Base
from sqlalchemy import Boolean, Column, Integer, Numeric, ForeignKey, String, Float



class SymbolInfomation(Base):
    __tablename__ = "SYMBOL_INFORMATION"

    id: int = Column("id", Integer, primary_key=True)
    account_id: int = Column("account_id", Integer, ForeignKey("ACCOUNT_CONFIG.id"), nullable=False)
    name: str = Column("name",String, nullable=False)
    digits: int = Column("digits", Integer, nullable=False)
    spread: int = Column("spread", Integer, nullable=False)
    select: bool = Column("select", Boolean, nullable=False)
    point: float = Column("point", Float, nullable=False)

    def __init__(self, account_id: int, name: str, digits: int, spread:int, select: bool, point: float):
        self.account_id = account_id
        self.name = name
        self.digits = digits
        self.spread = spread
        self.select = select
        self.point = point
        



