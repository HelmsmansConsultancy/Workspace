from .backend import Backend
from .money import Money
from sqlalchemy import Column, Integer, Numeric, String
from tabular.data.base import Base

class AccountConfig(Base):
    __tablename__ = "ACCOUNT_CONFIG"

    id: int = Column(Integer, primary_key=True)
    type: str = Column(String)
    description: str = Column(String)
    path: str = Column(String)
    backend: Backend = Column(String)
    money: Money = Column(Numeric(precision=10, scale=2), nullable=True)  
