from decimal import Decimal
from sqlalchemy import Boolean, Numeric, ForeignKey
from tabular.data.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class AccountStatus(Base):
    __tablename__ = "ACC_STAT"

    account_id: Mapped[int] = mapped_column("account_id", ForeignKey("ACC_CONF.id"), primary_key=True)

    balance: Mapped[Decimal] = mapped_column("balance", Numeric(12, 2), nullable=False)
    equity: Mapped[Decimal] = mapped_column("equity", Numeric(12, 2), nullable=False)
    profit: Mapped[Decimal] = mapped_column("profit", Numeric(12, 2), nullable=False)
    trade_allowed: Mapped[bool] = mapped_column("trade_allowed", Boolean, nullable=True)
    trade_expert: Mapped[bool] = mapped_column("trade_expert", Boolean, nullable=True)

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
        return f"<AS(account_id={self.account_id}, balance={self.balance}, equity={self.equity})>"
    
