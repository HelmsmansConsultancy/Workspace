from .backend import Backend
from .money import Money
from sqlalchemy import Column, Integer, Numeric, String
from tabular.data.base import Base

class AccountConfig(Base):
    __tablename__ = "ACCOUNT_CONFIG"

    id: int = Column(Integer, primary_key=True)
    login: int = Column(Integer, nullable=False)
    name: str = Column(String, nullable=False)
    server: str = Column(String, nullable=False)
    currency: str = Column(String, nullable=False)
    company: str = Column(String, nullable=False)

    def __init__(self, login: int, name: str, server: str, currency: str, company: str):
        self.login = login
        self.name = name
        self.server = server
        self.currency = currency
        self.company = company

    def __repr__(self):
        return f"<AccountConfig(id={self.id}, login={self.login}, name='{self.name}', server='{self.server}', currency='{self.currency}', company='{self.company}')>"
    
    def __str__(self):
        return f"<AccountConfig(id={self.id}, login={self.login}, name='{self.name}')>"
    
    
