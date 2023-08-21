from sqlalchemy import Column, String, Integer, MetaData, Boolean, false, not_, JSON
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
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(JSON)
    deleted = Column(Boolean)

    def __init__(self, name, address, deleted):
        self.name = name
        self.address = address
        self.deleted = deleted

    def __str__(self):
        return 'User: id:{0}, name:{1}, address: {2}'.format(self.id, self.name, self.address)



"""Uncomment following to create the table"""
Base.metadata.create_all(bind=engine)
print(f'Created the table')

session = scoped_session(sessionmaker(bind=engine))

employees = [
    ('A', {"state": "UP", "code":210431}),
    ('B', {"state": "UP", "code":210431}),
    ('D', {"state": "KA", "code":560068}),
    ('E', {"state": "KA", "code":560068}),
    ('F', {"state": "KA", "code":560048}),

]


for e in employees:
    employed = Employed(e[0], e[1],  False)
    session.add(employed)


session.commit()

# get all tables from the engine
meta = MetaData()
meta.reflect(bind=engine)
tables = meta.tables

# emp_table_obj = tables['employed']
# select_query = select([emp_table_obj.c.state, emp_table_obj.c.country, func.count(emp_table_obj.c.state)]
#                       ).where(not_(emp_table_obj.c.deleted)).group_by(emp_table_obj.c.state, emp_table_obj.c.country)
#
# conn = engine.connect()
# result = conn.execute(select_query)
# print(f'....................execute_result: {result}')
# employment_details = dict()
# for _row in result:
#     print(f'...................._row: {_row}')
#
#     state = _row[0]
#     country = _row[1]
#     count = _row[2]
#     print(state, country, count)
#     employment_details[(state, country)] = {
#         "employed": count
#     }
#
# print(f'employment_details: {employment_details}')
# un_emp_table_obj = tables['unemployed']
# #
# result = session.query(un_emp_table_obj.c.state, un_emp_table_obj.c.country, func.count(un_emp_table_obj.c.state)).group_by(un_emp_table_obj.c.state, un_emp_table_obj.c.country).all()
# print(result)
#
# for _row in result:
#     state = _row[0]
#     country = _row[1]
#     count = _row[2]
#     print(state, country, count)
#     state_country = (state, country)
#     if state_country in employment_details:
#         print(f' Found {state_country} in details')
#         employment_details[(state, country)].update({
#             "unemployed": count
#         })
#     else:
#         print(f' Not Found {state_country} in details')
#         employment_details[(state, country)] = {
#             "unemployed": count
#         }
#
# print(employment_details)
#
# events = []
# for k, v in employment_details.items():
#     events.append({
#         'state': k[0],
#         'country': k[1],
#         'employed': v['employed'],
#         'unemployed': v['unemployed']
#     })
#
# print(f'events: {events}')

"""
datum=# select * from employee;
 id | name |             address             | deleted
----+------+---------------------------------+---------
  1 | A    | {"state": "UP", "code": 210431} | f
  2 | B    | {"state": "UP", "code": 210431} | f
  3 | D    | {"state": "KA", "code": 560068} | f
  4 | E    | {"state": "KA", "code": 560068} | f
  5 | F    | {"state": "KA", "code": 560048} | f
(5 rows)



datum=# select address->>'state' as state, address->>'code' as code, count(*) from employee group by address->>'state',  address->>'code';
 state |  code  | count
-------+--------+-------
 KA    | 560068 |     2
 UP    | 210431 |     2
 KA    | 560048 |     1
(3 rows)




"""