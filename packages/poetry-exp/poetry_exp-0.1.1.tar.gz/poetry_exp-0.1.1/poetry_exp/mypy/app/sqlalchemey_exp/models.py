from base import Base
from sqlalchemy import Column, CHAR, String

class User(Base):
    __tablename__ = 'User'
    id = Column(CHAR(32), primary_key=True)
    name = Column(String(64))

