from typing import  Optional
from tabular.data.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
#from tabular.data.settings.account_status import AccountStatus
#from tabular.data.symbols.specific_symbol_info import SpecificSymbolInfomation

class AccountConfig(Base):
    __tablename__ = "ACC_CONF"

    id: Mapped[int] = mapped_column("id", primary_key=True)

#    accountStatus: Mapped[AccountStatus] = relationship(AccountStatus, back_populates="accountConfig", uselist=False)
#    specificSymbolInfomations: Mapped[set[SpecificSymbolInfomation]] = relationship()

    account_login: Mapped[int] = mapped_column("login")
    trade_mode: Mapped[Optional[int]] = mapped_column("trade_mode" )
    company: Mapped[str] = mapped_column("company")
    currency: Mapped[str] = mapped_column("currency")

    leverage: Mapped[Optional[int]] = mapped_column("leverage")

    password: Mapped[Optional[str]] = mapped_column("password")
    name: Mapped[str] = mapped_column("name")
    server: Mapped[str] = mapped_column("server")

    def __init__(self, company: str, currency: str, leverage: int, account_login: int, name: str, password: str, server: str, trade_mode: int):
        self.company = company
        self.currency = currency
        self.leverage = leverage
        self.account_login = account_login
        self.name = name
        self.password = password
        self.server = server
        self.trade_mode = trade_mode

    def __repr__(self):
        return f"<AccountConfig(id={self.id}, login={self.account_login}, name='{self.name}', password='{bool(self.password)}', server='{self.server}', currency='{self.currency}', company='{self.company}')>"
    
    def __str__(self):
        return f"<AccountConfig(id={self.id}, login={self.account_login}, name='{self.name:.20}')>"
    
    
