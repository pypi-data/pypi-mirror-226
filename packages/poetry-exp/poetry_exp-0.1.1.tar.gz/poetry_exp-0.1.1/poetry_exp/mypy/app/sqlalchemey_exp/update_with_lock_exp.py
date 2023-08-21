from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import os, time



Base = declarative_base()


class Customer(Base):
    __tablename__ = "customer"
    id       = Column(Integer, primary_key=True)
    name     = Column(String, nullable=False)
    balance    = Column(Integer)

DB_CONFIG = {
    "drivername": "postgresql",
    "database": "datum",
    "username": "datum",
    "password": "hpinvent",
    "host": "127.0.0.1"
}

engine = create_engine(URL(**DB_CONFIG))
sm = sessionmaker()
sm.configure(bind=engine)

session = sm()

customer = session.query(Customer).filter_by(id=1).with_for_update(of=Customer).one()
print(f'[Main-Thread] [PID: {os.getpid()}] Balance: {customer.balance} for customer id: {customer.id}')
customer.balance = 222
session.add(customer)
print(f'[Main-Thread] [PID: {os.getpid()}] Updating balance...')
time.sleep(30)

session.commit()
print(f'[Main-Thread] [PID: {os.getpid()}] Update committed...')

session.flush()
session.close()


"""

Get the locks:
datum=#  select pid, state,query from pg_stat_activity where pid in ( select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');
(0 rows)

datum=#

[root@Aafak-Local-CD-DO-May18 aafak]# python3 update_with_lock_exp.py
[Main-Thread] [PID: 850] Balance: 113 for customer id: 1
[Main-Thread] [PID: 850] Updating balance...


datum=#  select pid, state,query from pg_stat_activity where pid in (  select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');
-[ RECORD 1 ]---------------------------------------------------------------------------------------------------
pid   | 1768
state | idle in transaction
query | SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance +
      | FROM customer                                                                                           +
      | WHERE customer.id = 1 FOR UPDATE OF customer

datum=# select pid, mode, relname from pg_locks l join pg_class t on l.relation = t.oid and t.relkind = 'r' where t.relname = 'customer';
-[ RECORD 1 ]---------
pid     | 1768
mode    | RowShareLock
relname | customer

datum=#



[Main-Thread] [PID: 850] Update committed...
You have mail in /var/spool/mail/root
[root@Aafak-Local-CD-DO-May18 aafak]#


datum=#  select pid, state,query from pg_stat_activity where pid in (  select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');
(0 rows)

datum=#

"""