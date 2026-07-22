from tabular.data.base.base import Base
from tabular.data.symbols.generic_symbol_info import GenericSymbolInfomation
from tabular.data.settings.account_config import AccountConfig
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class SpecificSymbolInfomation(Base):
    __tablename__ = "SPECIFIC_SYMBOL_INFORMATION"

    id: Mapped[int] = mapped_column("id", primary_key=True)

    account_id: Mapped[int] = Column("account_id", ForeignKey("ACCOUNT_CONFIG.id"), nullable=False)
    accountConfig: Mapped[AccountConfig] =  relationship(AccountConfig, back_populates="genericSymbolInfomation")

    symbol_id: Mapped[int] = Column("symbol_id", ForeignKey("GENERIC_SYMBOL_INFORMATION.id"), nullable=False)
    genericSymbolInfomation: Mapped[GenericSymbolInfomation] = relationship(GenericSymbolInfomation, back_populates="genericSymbolInfomation")

    name: Mapped[str] = mapped_column("name", nullable=False)
    symbol: Mapped[str] = mapped_column("symbol", nullable=False)
    digits: Mapped[int] = mapped_column("digits", nullable=False)
    spread: Mapped[int] = mapped_column("spread", nullable=False)
    select: Mapped[bool] = mapped_column("select", nullable=False)
    point: Mapped[float] = mapped_column("point", nullable=False)

    def __init__(self, account_id: int):
        self.account_id = account_id

    def __repr__(self):
        return f"<SymbolInfomation(id={self.id}, account_id={self.account_id}, symbol={self.symbol} name={self.name} digits={self.digits}, spread={self.spread}, select={self.select}, point={self.point})>"
        
    
    def __str__(self):
        return f"<SymbolInfomation(id={self.id} name={self.name}, digits={self.digits},  point={self.point}, symbol={self.symbol})>"



