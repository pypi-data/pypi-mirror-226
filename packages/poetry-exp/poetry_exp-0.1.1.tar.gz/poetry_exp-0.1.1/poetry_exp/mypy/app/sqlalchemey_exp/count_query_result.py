from sqlalchemy import Column, String, Integer, MetaData, Boolean, false, not_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import func, select

from sqlalchemy.orm import (
    sessionmaker,
    scoped_session)

DB_CONN_URL = 'postgresql://datum:hpinvent@127.0.0.1/datum'

engine = create_engine(DB_CONN_URL)
print(engine)

Base = declarative_base()


class Employed(Base):
    __tablename__ = 'employed'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)
    country = Column(String)
    deleted = Column(Boolean)

    def __init__(self, name, state, country, deleted):
        self.name = name
        self.state = state
        self.country = country
        self.deleted = deleted

    def __str__(self):
        return 'User: id:{0}, name:{1}'.format(self.id, self.name)


class UnEmployed(Base):
    __tablename__ = 'unemployed'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)
    country = Column(String)
    deleted = Column(Boolean)


    def __init__(self, name, state, country, deleted):
        self.name = name
        self.state = state
        self.country = country
        self.deleted = deleted

    def __str__(self):
        return 'User: id:{0}, name:{1}'.format(self.id, self.name)


"""Uncomment following to create the table"""
# Base.metadata.create_all(bind=engine)
print(f'Created the table')

session = scoped_session(sessionmaker(bind=engine))

employeds = [
    ('A', 'UP', 'India'),
    ('B', 'MP', 'India'),
    ('C', 'UP', 'India'),
    ('D', 'HP', 'India'),
    ('E', 'UP', 'India'),
    ('F', 'MP', 'India'),
    ('G', 'New York', 'USA'),
    ('H', 'Texas', 'USA'),
    ('I', 'Washington', 'USA'),
    ('J', 'New York', 'USA'),
    ('K', 'Texas', 'USA'),
    ('L', 'New York', 'USA')
]

un_employeds = [
    ('M', 'UP', 'India'),
    ('N', 'MP', 'India'),
    ('O', 'UP', 'India'),
    ('P', 'HP', 'India'),
    ('Q', 'UP', 'India'),
    ('R', 'MP', 'India'),
    ('S', 'New York', 'USA'),
    ('T', 'Texas', 'USA'),
    ('U', 'Washington', 'USA'),
    ('V', 'New York', 'USA'),
    ('S', 'Texas', 'USA'),
    ('T', 'New York', 'USA'),
    ('U', 'UP', 'India'),
    ('V', 'UP', 'India'),
    ('X', 'MP', 'India'),
    ('Y', 'MP', 'India'),
    ('Z', 'HP', 'India'),
    ('AA', 'New York', 'USA'),
    ('BB', 'New York', 'USA'),
    ('CC', 'Texas', 'USA'),
    ('DD', 'Texas', 'USA'),
    ('EE', 'Texas', 'USA'),
]

for e in employeds:
    employed = Employed(e[0], e[1], e[2], False)
    session.add(employed)


for ue in un_employeds:
    u_employed = UnEmployed(ue[0], ue[1], ue[2], False)
    session.add(u_employed)

# session.commit()

# get all tables from the engine
meta = MetaData()
meta.reflect(bind=engine)
tables = meta.tables

emp_table_obj = tables['employed']
select_query = select([func.count()]
                      ).where(emp_table_obj.c.state == 'UP' and
                              emp_table_obj.c.name == 'A' and
                              not_(emp_table_obj.c.deleted))

conn = engine.connect()
result = conn.execute(select_query).scalar()
print(f'....................execute_result: {result}')
#print(f'....................count: {select_query.count()}')
#
# for _row in result:
#     print(f'...................._row: {_row}')
#     state = _row[0]
#     country = _row[1]
#     print(state, country)


"""
datum=# select * from employed;
 id | name |   state    | country | deleted
----+------+------------+---------+---------
  1 | A    | UP         | India   | f
  2 | B    | MP         | India   | f
  3 | C    | UP         | India   | f
  4 | D    | HP         | India   | f
  5 | E    | UP         | India   | f
  6 | F    | MP         | India   | f
  7 | G    | New York   | USA     | f
  8 | H    | Texas      | USA     | f
  9 | I    | Washington | USA     | f
 10 | J    | New York   | USA     | f
 11 | K    | Texas      | USA     | f
 12 | L    | New York   | USA     | f
(12 rows)

                                                         ^
datum=# select state, country, count(country) from employed where deleted=false group by state,country;
   state    | country | count
------------+---------+-------
 New York   | USA     |     3
 Washington | USA     |     1
 HP         | India   |     1
 Texas      | USA     |     2
 MP         | India   |     2
 UP         | India   |     3
(6 rows)

datum=#



[root@Atlas-CBT-Nov30 aafak]# python3.6 group_by_count_exp4.py
Engine(postgresql://datum:***@127.0.0.1/datum)
Created the table
[('New York', 'USA', 3), ('Washington', 'USA', 1), ('HP', 'India', 1), ('Texas', 'USA', 2), ('MP', 'India', 2), ('UP', 'India', 3)]
New York USA 3
Washington USA 1
HP India 1
Texas USA 2
MP India 2
UP India 3
employment_details: {('New York', 'USA'): {'employed': 3}, ('Washington', 'USA'): {'employed': 1}, ('HP', 'India'): {'employed': 1}, ('Texas', 'USA'): {'employed': 2}, ('MP', 'India'): {'employed': 2}, ('UP', 'India'): {'employed': 3}}
[('New York', 'USA', 5), ('Washington', 'USA', 1), ('HP', 'India', 2), ('Texas', 'USA', 5), ('MP', 'India', 4), ('UP', 'India', 5)]
New York USA 5
 Found ('New York', 'USA') in details
Washington USA 1
 Found ('Washington', 'USA') in details
HP India 2
 Found ('HP', 'India') in details
Texas USA 5
 Found ('Texas', 'USA') in details
MP India 4
 Found ('MP', 'India') in details
UP India 5
 Found ('UP', 'India') in details
{('New York', 'USA'): {'employed': 3, 'unemployed': 5}, ('Washington', 'USA'): {'employed': 1, 'unemployed': 1}, ('HP', 'India'): {'employed': 1, 'unemployed': 2}, ('Texas', 'USA'): {'employed': 2, 'unemployed': 5}, ('MP', 'India'): {'employed': 2, 'unemployed': 4}, ('UP', 'India'): {'employed': 3, 'unemployed': 5}}
events: [{'state': 'New York', 'country': 'USA', 'employed': 3, 'unemployed': 5}, {'state': 'Washington', 'country': 'USA', 'employed': 1, 'unemployed': 1}, {'state': 'HP', 'country': 'India', 'employed': 1, 'unemployed': 2}, {'state': 'Texas', 'country': 'USA', 'employed': 2, 'unemployed': 5}, {'state': 'MP', 'country': 'India', 'employed': 2, 'unemployed': 4}, {'state': 'UP', 'country': 'India', 'employed': 3, 'unemployed': 5}]
You have mail in /var/spool/mail/root
[root@Atlas-CBT-Nov30 aafak]#


"""