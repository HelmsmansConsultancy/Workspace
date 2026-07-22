from tabular.data.base.base import Base
from tabular.data.symbols.specific_symbol_info import SpecificSymbolInfomation
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class GenericSymbolInfomation(Base):
    __tablename__ = "GENERIC_SYMBOL_INFORMATION"

    specificSymbolInfomations: Mapped[list[SpecificSymbolInfomation]] = relationship(SpecificSymbolInfomation, back_populates="specificSymbolInfomations")

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column("symbol",String, nullable=False)
    digits: Mapped[int] = mapped_column("digits", Integer, nullable=False)
    point: Mapped[float] = mapped_column("point", Float, nullable=False)

    def __init__(self, account_id: int):
        self.account_id = account_id

    def __repr__(self):
        return f"<GenericSymbolInfomation(id={self.id}, symbol={self.symbol}, digits={self.digits},  point={self.point})>"
        
    
    def __str__(self):
        return f"<GSI(id={self.id}, symbol={self.symbol}, digits={self.digits})>"



