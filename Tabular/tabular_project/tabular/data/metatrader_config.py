from sqlalchemy import Column, Integer, String
from tabular.data.base import Base


class MetatraderConfig(Base):
    __tablename__ = "metatrader_config"

    id: int             = Column(Integer,   primary_key=True, nullable=False, autoincrement=True)
    path: str           = Column(String,    nullable=False)
    terminal_version: str = Column(String,  nullable=True)
    build: str          = Column(String,    nullable=True)
    release_date: str   = Column(String,    nullable=True)
    
    def __init__(self, id: int = None, path: str = None):
        self.id = id
        self.path = path

    def __repr__(self):
        return f"<MetatraderConfig(id={self.id}, path='{self.path}', terminal_version='{self.terminal_version}', build='{self.build}', release_date='{self.release_date}')>"