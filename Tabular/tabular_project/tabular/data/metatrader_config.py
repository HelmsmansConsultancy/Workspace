from sqlalchemy import Boolean, Column, Integer, String
from tabular.data.base import Base


class MetatraderConfig(Base):
    __tablename__ = "METATRADER_CONFIG"

    id: int             = Column(Integer,   primary_key=True, nullable=False, autoincrement=True)
    path: str           = Column(String,    nullable=False)

    trade_allowed: bool         = Column(Boolean,   nullable=True)
    tradeapi_disabled: bool      = Column(Boolean,   nullable=True)
    notifications_enabled: bool   = Column(Boolean,   nullable=True)
    mqid: bool                 = Column(Boolean,   nullable=True)

    terminal_version: str = Column(String,  nullable=True)
    build: str          = Column(String,    nullable=True)
    release_date: str   = Column(String,    nullable=True)
    
    def __init__(self, id: int = None, path: str = None):
        self.id = id
        self.path = path

    def __repr__(self):
        return f"<MetatraderConfig(id={self.id}, path='{self.path}', trade_allowed={self.trade_allowed}, tradeapi_disabled={self.tradeapi_disabled}, notifications_enabled={self.notifications_enabled}, mqid={self.mqid}, terminal_version='{self.terminal_version}', build='{self.build}', release_date='{self.release_date}')>"
    

    def __str__(self):
        return f"<MetatraderConfig(id={self.id}, path='{self.path}')>"
    
