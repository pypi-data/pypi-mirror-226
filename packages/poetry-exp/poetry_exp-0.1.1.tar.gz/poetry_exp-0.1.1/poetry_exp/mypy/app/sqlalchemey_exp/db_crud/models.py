from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Backups(Base):
    __tablename__ = 'backups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    backup_type = Column(String)  # Just adding new attributes here will not add the column in database
    """
    mycloud=# alter table backups add column backup_type varchar;
    ALTER TABLE
    mycloud=#
    """