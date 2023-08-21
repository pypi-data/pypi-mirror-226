from sqlalchemy import (
     create_engine,
     Integer,
     String,
     Column,
     inspect
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL


Base = declarative_base()
sqlite_db = {
    'drivername': 'sqlite',
    'database': 'dbs//create_table_from_class'
}

engine = create_engine(URL(**sqlite_db))

class Emp(Base):
    __tablename__ = 'emp'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


Base.metadata.create_all(bind=engine)

ins = inspect(engine)

for table in ins.get_table_names():
    print (table)

# Todo Find a way to create table if not exists


