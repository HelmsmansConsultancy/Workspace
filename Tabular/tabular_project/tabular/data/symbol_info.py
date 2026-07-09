from tabular.data.base import Base
from sqlalchemy import Boolean, Column, Integer, Numeric, ForeignKey, String



class SymbolInfo(Base):
    __tablename__ = "SYMBOL_INFO"

    id: int = Column("id", Integer, primary_key=True)
    account_id: int = Column("account_id", Integer, ForeignKey("ACCOUNT_CONFIG.id"), nullable=False)
    name: str = Column("name",String, nullable=False)
    digits: int = Column("digits", Integer, nullable=False)
    select: bool = Column("select", Boolean, nullable=False)

    def __init__(self, account_id: int, name: str, digits: int, select: bool):
        self.account_id = account_id
        self.name = name
        self.digits = digits
        self.select = select
        



