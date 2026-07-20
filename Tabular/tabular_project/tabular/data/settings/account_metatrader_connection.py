from sqlalchemy import  Column, Integer, ForeignKey
from tabular.data.base.base import Base

class AccountMetatraderConnection(Base):
    __tablename__ = "ACCOUNT_METATRADER_CONNECTION"

    account_id: int = Column("acount_id", Integer, ForeignKey("ACCOUNT_CONFIG.id"), primary_key=True)
    metatrader_id: int = Column("metatrader_id", Integer, ForeignKey("METATRADER_CONFIG.id"), primary_key=True)

    def __init__(self, account_id: int, metatrader_id: int):
        self.account_id = account_id
        self.metatrader_id = metatrader_id

    def __str__(self):
        return f"<AccountMetatraderConnection(account_id={self.account_id}, metatrader_id={self.metatrader_id})"
