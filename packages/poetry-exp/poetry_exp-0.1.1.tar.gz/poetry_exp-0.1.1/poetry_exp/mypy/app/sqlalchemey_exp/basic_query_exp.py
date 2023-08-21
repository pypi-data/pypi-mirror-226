from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import or_
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

db_url = {'drivername': 'sqlite',
           'database':'dbs\\basic_query'
          }

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    id       = Column(Integer, primary_key=True)
    name     = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    birth    = Column(DateTime)

# create tables
engine = create_engine(URL(**db_url))
Base.metadata.create_all(bind=engine)

users = [
    User(name='ed',
         fullname='Ed Jones',
         birth=datetime(1989,7,1)),
    User(name='wendy',
         fullname='Wendy Williams',
         birth=datetime(1983,4,1)),
    User(name='mary',
         fullname='Mary Contrary',
         birth=datetime(1990,1,30)),
    User(name='fred',
         fullname='Fred Flinstone',
         birth=datetime(1977,3,12)),
    User(name='justin',
         fullname="Justin Bieber")]

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# add_all
session.add_all(users)
session.commit()

print("----> order_by(id):")
query = session.query(User).order_by(User.id)
for _row in query.all():
    print(_row.name, _row.fullname, _row.birth)

print("\n----> order_by(desc(id)):")
query = session.query(User).order_by(desc(User.id))
for _row in query.all():
    print(_row.name, _row.fullname, _row.birth)

print("\n----> order_by(date):")
query = session.query(User).order_by(User.birth)
for _row in query.all():
    print(_row.name, _row.fullname, _row.birth)

print("\n----> EQUAL:")
query = session.query(User).filter(User.id == 2)
_row = query.first()
print(_row.name, _row.fullname, _row.birth)

print("\n----> NOT EQUAL:")
query = session.query(User).filter(User.id != 2)
for _row in query.all():
    print(_row.name, _row.fullname, _row.birth)

print("\n----> IN:")
query = session.query(User).filter(User.name.in_(['ed', 'wendy']))
for _row in query.all():
    print(_row.name, _row.fullname, _row.birth)

print("\n----> NOT IN:")
query = session.query(User).filter(~User.name.in_(['ed', 'wendy']))
for _row in query.all():
    print(_row.name, _row.fullname, _row.birth)

print("\n----> AND:")
query = session.query(User).filter(
        User.name=='ed', User.fullname=='Ed Jones')
_row = query.first()
print(_row.name, _row.fullname, _row.birth)

print("\n----> OR:")
query = session.query(User).filter(
        or_(User.name=='ed', User.name=='wendy'))
for _row in query.all():
    print(_row.name, _row.fullname, _row.birth)

print("\n----> NULL:")
query = session.query(User).filter(User.birth == None)
for _row in query.all():
    print(_row.name, _row.fullname)

print("\n----> NOT NULL:")
query = session.query(User).filter(User.birth != None)
for _row in query.all():
    print(_row.name, _row.fullname)

print("\n----> LIKE")
query = session.query(User).filter(User.name.like('%ed%'))
for _row in query.all():
    print(_row.name, _row.fullname)