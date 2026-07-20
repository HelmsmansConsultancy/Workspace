import os
from sqlalchemy import Column, Integer, String
from tabular.data.base.base import Base

class ApplicationConfig(Base):
    __tablename__ = "APPLICATION_CONFIG"

    id: int = Column(Integer, primary_key=True)
    db_file: str = Column(String)

    def __init__(self):
        self.db_file = os.getcwd()  + ".db"
    



