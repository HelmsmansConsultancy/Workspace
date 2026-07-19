from sqlalchemy import  Column, Integer, String
from tabular.data.base import Base

class AccountConfig(Base):
    __tablename__ = "ACCOUNT_CONFIG"

    id: int = Column("id", Integer, primary_key=True)
    company: str = Column("company", String, nullable=False)
    currency: str = Column("currency", String, nullable=False)
    leverage: int = Column("leverage", Integer, nullable=True)
    account_login: int = Column("login", Integer, nullable=False)
    name: str = Column("name", String, nullable=False)
    password: str = Column("password", String, nullable=True)
    server: str = Column("server", String, nullable=False)
    trade_mode: int = Column("trade_mode", Integer, nullable=True)

    def __init__(self, company: str, currency: str, leverage: int, account_login: int, name: str, server: str, trade_mode: int):
        self.company = company
        self.currency = currency
        self.leverage = leverage
        self.account_login = account_login
        self.name = name
        self.server = server
        self.trade_mode = trade_mode

    def __repr__(self):
        return f"<AccountConfig(id={self.id}, login={self.account_login}, name='{self.name}', password='{bool(self.password)}', server='{self.server}', currency='{self.currency}', company='{self.company}')>"
    
    def __str__(self):
        return f"<AccountConfig(id={self.id}, login={self.account_login}, name='{self.name}')>"
    
    
