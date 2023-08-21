from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password = Column(String)


class HypervisorManager(Base):
    __tablename__ = 'hypervisor_managers'
    id = Column(String, primary_key=True)
    name = Column(String)
    ip_address = Column(String)
    username = Column(String)
    password = Column(String)