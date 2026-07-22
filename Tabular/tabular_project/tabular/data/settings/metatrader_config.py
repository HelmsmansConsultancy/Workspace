from typing import  Optional
from tabular.data.base.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class MetatraderConfig(Base):
    __tablename__ = "METATRADER_CONFIG"

    id: Mapped[int]             = mapped_column("id",   primary_key=True,  autoincrement=True)

    name: Mapped[str]           = mapped_column()
    path: Mapped[str]           = mapped_column()

    trade_allowed: Mapped[Optional[bool]]         = mapped_column()
    tradeapi_disabled: Mapped[Optional[bool]]      = mapped_column()
    notifications_enabled: Mapped[Optional[bool]]   = mapped_column()
    mqid: Mapped[Optional[bool]]                 = mapped_column()

    terminal_version: Mapped[Optional[str]] = mapped_column()
    build: Mapped[Optional[str]]          = mapped_column()
    release_date: Mapped[Optional[str]]   = mapped_column()
    
    def __init__(self, id: int = None, path: str = None, name: str = None):
        self.id = id
        self.path = path
        self.name = name

    def __repr__(self):
        return f"<MetatraderConfig(id={self.id}, name='{self.name}', path='{self.path}', trade_allowed={self.trade_allowed}, tradeapi_disabled={self.tradeapi_disabled}, notifications_enabled={self.notifications_enabled}, mqid={self.mqid}, terminal_version='{self.terminal_version}', build='{self.build}', release_date='{self.release_date}')>"
    

    def __str__(self):
        return f"<MetatraderConfig(id={self.id}, name='{self.name}')>"
    
