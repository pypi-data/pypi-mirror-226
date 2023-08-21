from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime, MetaData
from sqlalchemy import or_
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    scoped_session)

db_url = {'drivername': 'postgresql',
           'datum':'dbs\\basic_query',
           'host': '172.17.29.166',
           'username': 'postgres',
           'password': 'postgres'
          }

DB_CONN_URL = 'postgresql://datum:hpinvent@127.0.0.1/datum'
#DB_CONN_URL = 'postgresql://datum:hpinvent@172.17.29.166/datum'

engine = create_engine(DB_CONN_URL)
print(engine)

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'emp3'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)
    country = Column(String)

    def __init__(self, name, state, country):
        self.name = name
        self.state = state
        self.country = country

    def __str__(self):
        return 'User: id:{0}, name:{1}'.format(self.id, self.name)

"""Uncomment following to create the table"""
Base.metadata.create_all(bind=engine)
#print(f'Created the table')




session = scoped_session(sessionmaker(bind=engine))

#Insert records
e1 = Employee('A', 'UP', 'India')
session.add(e1)
session.commit()

e1 = Employee('B', 'MP', 'India')
session.add(e1)
session.commit()

e1 = Employee('C', 'UP', 'India')
session.add(e1)
session.commit()

e1 = Employee('D', 'HP', 'India')
session.add(e1)
session.commit()

e1 = Employee('E', 'UP', 'India')
session.add(e1)
session.commit()

e1 = Employee('F', 'MP', 'India')
session.add(e1)
session.commit()


e1 = Employee('G', 'New York', 'USA')
session.add(e1)
session.commit()

e1 = Employee('H', 'Texas', 'USA')
session.add(e1)
session.commit()

e1 = Employee('I', 'Washington', 'USA')
session.add(e1)
session.commit()

e1 = Employee('J', 'New York', 'USA')
session.add(e1)
session.commit()

e1 = Employee('K', 'Texas', 'USA')
session.add(e1)
session.commit()

e1 = Employee('L', 'New York', 'USA')
session.add(e1)
session.commit()

# get all tables from the engine
meta = MetaData()
meta.reflect(bind=engine)
tables = meta.tables

emp_table_obj = tables['emp3']
#
from sqlalchemy import func
result = session.query(emp_table_obj.c.state, emp_table_obj.c.country, func.count(emp_table_obj.c.state)).group_by(emp_table_obj.c.state, emp_table_obj.c.country).all()
print(result)  # [('HP', 1), ('UP', 4), ('MP', 1)]

for _row in result:
    state = _row[0]
    country = _row[1]
    count = _row[2]
    print(state, country, count)
