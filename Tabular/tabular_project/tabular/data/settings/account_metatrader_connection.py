from sqlalchemy import ForeignKey
from tabular.data.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class AccountMetatraderConnection(Base):
    __tablename__ = "ACC_MT_CONN"

    account_id: Mapped[int] = mapped_column("acount_id", ForeignKey("ACC_CONF.id"), primary_key=True)
    metatrader_id: Mapped[int] = mapped_column("metatrader_id", ForeignKey("MT_CONF.id"), primary_key=True)

    def __init__(self, account_id: int, metatrader_id: int):
        self.account_id = account_id
        self.metatrader_id = metatrader_id

    def __str__(self):
        return f"<AccountMetatraderConnection(account_id={self.account_id}, metatrader_id={self.metatrader_id})"
