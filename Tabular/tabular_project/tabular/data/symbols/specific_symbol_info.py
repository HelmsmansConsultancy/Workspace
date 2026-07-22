from tabular.data.base import Base
#from tabular.data.settings.account_config import AccountConfig
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
#from tabular.data.symbols.generic_symbol_info import GenericSymbolInfomation

class SpecificSymbolInfomation(Base):
    __tablename__ = "SPEC_SYMBOL_INFO"

    id: Mapped[int] = mapped_column("id", primary_key=True)

    account_id: Mapped[int] = mapped_column("account_id", ForeignKey("ACC_CONF.id"))
#   accountConfig: Mapped[AccountConfig] =  relationship(AccountConfig, back_populates="genericSymbolInfomation")

    symbol_id: Mapped[int] = mapped_column("symbol_id", ForeignKey("GEN_SYMBOL_INFO.id"))
#   genericSymbolInfomation: Mapped[GenericSymbolInfomation] = relationship(GenericSymbolInfomation, back_populates="genericSymbolInfomation")

    name: Mapped[str] = mapped_column("name")
    symbol: Mapped[str] = mapped_column("symbol")
    digits: Mapped[int] = mapped_column("digits")
    spread: Mapped[int] = mapped_column("spread")
    select: Mapped[bool] = mapped_column("select")
    point: Mapped[float] = mapped_column("point")

    def __init__(self, account_id: int):
        self.account_id = account_id

    def __repr__(self):
        return f"<SymbolInfomation(id={self.id}, account_id={self.account_id}, symbol={self.symbol} name={self.name} digits={self.digits}, spread={self.spread}, select={self.select}, point={self.point})>"
        
    
    def __str__(self):
        return f"<SymbolInfomation(id={self.id} name={self.name}, digits={self.digits},  point={self.point}, symbol={self.symbol})>"



