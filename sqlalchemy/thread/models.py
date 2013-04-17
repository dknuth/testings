from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String)

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    age = Column(Integer)
    seq = Column(Integer)

    def __init__(self, name, age, seq=0):
        self.name = name
        self.age = age
        self.seq = seq
