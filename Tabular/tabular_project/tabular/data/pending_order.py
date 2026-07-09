from tabular.data.base import Base
from sqlalchemy import Boolean, Column, Integer, Numeric, ForeignKey, String



class PendingOrder(Base):
    __tablename__ = "PENDING_ORDER"

    id: int = Column("id", Integer, primary_key=True)
    account_id: int = Column("account_id", Integer, ForeignKey("ACCOUNT_CONFIG.id"), nullable=False)



