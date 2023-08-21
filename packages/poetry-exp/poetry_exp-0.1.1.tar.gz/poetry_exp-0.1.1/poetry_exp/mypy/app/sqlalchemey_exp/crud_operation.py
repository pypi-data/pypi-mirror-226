from sqlalchemy.orm import sessionmaker
import time
import os
from sqlalchemy import create_engine, MetaData, update, select
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError


from threading import Thread

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id       = Column(Integer, primary_key=True)
    name     = Column(String, nullable=False)
    balance    = Column(Integer)

DB_CONN_URL = 'postgresql://datum:hpinvent@127.0.0.1/datum'
engine = create_engine(DB_CONN_URL)

meta = MetaData()
meta.reflect(bind=engine)
TABLES = meta.tables


# Run first time only
# sm = sessionmaker()
# sm.configure(bind=engine)
# s = sm()
# Base.metadata.create_all(bind=engine)
#
# customers = [
#     Customer(name='John',
#          balance=0)
#     ]
# s.add_all(customers)
# s.commit()

# customer = s.query(Customer).get(1)
# print(f'[Main-Thread] Balance: {customer.balance} for customer id: {customer.id}')


def get_records(table_name, cid):
    table_obj = TABLES[table_name]
    q = select([table_obj]).where((table_obj.c.id==cid))
    with engine.connect() as con:
        result = con.execute(q)
        # print(f'@@@@@@@@@@@@@result: {result}')
        # print(f'@@@@@@@@@@@@@result: {result.rowcount}')
        if not result.rowcount:
            print(f'No records found for resource: {table_name} with cid: {cid}')
        return [dict(row) for row in result][0] if result.rowcount else dict()


def update_record(table_name, cid, balance):
    table_obj = TABLES[table_name]
    q = update(table_obj).where((table_obj.c.id==cid)).values(balance=balance)
    with engine.connect() as con:
        con.execute(q)



if __name__ == '__main__':
    customer = get_records('customer', 1)
    print(customer)
    update_record('customer', 1, 1)
    customer = get_records('customer', 10)
    print(customer)




"""

"""