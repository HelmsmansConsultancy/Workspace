from tabular.data.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
#from tabular.data.symbols.specific_symbol_info import SpecificSymbolInfomation

class GenericSymbolInfomation(Base):
    __tablename__ = "GEN_SYMBOL_INFO"

#    specificSymbolInfomations: Mapped[set[SpecificSymbolInfomation]] = relationship(back_populates="specificSymbolInfomations")

    id: Mapped[int] = mapped_column("id", primary_key=True)
    symbol: Mapped[str] = mapped_column("symbol")
    digits: Mapped[int] = mapped_column("digits")
    point: Mapped[float] = mapped_column("point")

    def __init__(self, account_id: int):
        self.account_id = account_id

    def __repr__(self):
        return f"<GenericSymbolInfomation(id={self.id}, symbol={self.symbol}, digits={self.digits},  point={self.point})>"
        
    
    def __str__(self):
        return f"<GSI(id={self.id}, symbol={self.symbol}, digits={self.digits})>"



