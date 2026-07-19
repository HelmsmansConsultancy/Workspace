from decimal import Decimal
from sqlalchemy import Boolean, Column, Integer, Numeric, ForeignKey
from tabular.data.base import Base

class AccountStatus(Base):
    __tablename__ = "ACCOUNT_STATUS"

    account_id: int = Column("account_id", Integer, ForeignKey("ACCOUNT_CONFIG.id"), primary_key=True)
    balance: Decimal = Column("balance", Numeric(12, 2), nullable=False)
    equity: Decimal = Column("equity", Numeric(12, 2), nullable=False)
    profit: Decimal = Column("profit", Numeric(12, 2), nullable=False)
    trade_allowed: bool = Column("trade_allowed", Boolean, nullable=True)
    trade_expert: bool = Column("trade_expert", Boolean, nullable=True)

    def __init__(self, account_id: int, balance: Decimal, equity: Decimal, profit: Decimal, trade_allowed: bool, trade_expert: bool):
        self.account_id = account_id
        self.balance = balance
        self.equity = equity
        self.profit = profit
        self.trade_allowed = trade_allowed
        self.trade_expert = trade_expert

    def __repr__(self):
        return f"<AccountStatus(account_id={self.account_id}, trade_allowed={self.trade_allowed}, trade_expert={self.trade_expert}, balance={self.balance}, equity={self.equity}, Running profit={self.profit})>"

    def __str__(self):
        return f"<AccountStatus(account_id={self.account_id}, balance={self.balance}, equity={self.equity})>"
    
