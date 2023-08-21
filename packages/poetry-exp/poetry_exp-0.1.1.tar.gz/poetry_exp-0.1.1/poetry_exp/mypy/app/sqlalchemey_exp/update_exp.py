from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import os


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

customer = session.query(Customer).get(1)
print(f'[Main-Thread] [PID: {os.getpid()}] Balance: {customer.balance} for customer id: {customer.id}')

customer.balance = 111
session.add(customer)
print(f'[Main-Thread] [PID: {os.getpid()}] Updating balance...')

session.commit()
print(f'[Main-Thread] [PID: {os.getpid()}] Update committed...')

session.flush()
session.close()



"""
First set the balance 0
datum=# update customer set balance=0;
UPDATE 1

******************then check the locks:  so no lock here
datum=#  select pid, state,query from pg_stat_activity where pid in (  select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');                                                                   (0 rows)

datum=# select pid, mode, relname from pg_locks l join pg_class t on l.relation = t.oid and t.relkind = 'r' where t.relname = 'customer';
(0 rows)

datum=#


Run first: 
[root@Aafak-Local-CD-DO-May18 aafak]# python3 update_with_lock_exp.py
[Main-Thread] [PID: 1157] Balance: 222 for customer id: 1
[Main-Thread] [PID: 1157] Updating balance...

********************now check locks: Now you can see, there is a update oock
datum=# select pid, mode, relname from pg_locks l join pg_class t on l.relation = t.oid and t.relkind = 'r' where t.relname = 'customer';
-[ RECORD 1 ]---------
pid     | 2588
mode    | RowShareLock
relname | customer

datum=#  select pid, state,query from pg_stat_activity where pid in (  select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');
-[ RECORD 1 ]---------------------------------------------------------------------------------------------------
pid   | 2588
state | idle in transaction
query | SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance +
      | FROM customer                                                                                           +
      | WHERE customer.id = 1 FOR UPDATE OF customer


now run :
[root@Aafak-Local-CD-DO-May18 aafak]# python3 update_exp.py
[Main-Thread] [PID: 1161] Balance: 222 for customer id: 1
[Main-Thread] [PID: 1161] Updating balance...

*****************now check the locks: you can see now more locks, now its waiting for lock to be released
datum=# select pid, mode, relname from pg_locks l join pg_class t on l.relation = t.oid and t.relkind = 'r' where t.relname = 'customer';
-[ RECORD 1 ]-------------
pid     | 2588
mode    | RowShareLock
relname | customer
-[ RECORD 2 ]-------------
pid     | 2613
mode    | AccessShareLock
relname | customer
-[ RECORD 3 ]-------------
pid     | 2613
mode    | RowExclusiveLock
relname | customer
-[ RECORD 4 ]-------------
pid     | 2613
mode    | ExclusiveLock
relname | customer

datum=#  select pid, state,query from pg_stat_activity where pid in (  select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');
-[ RECORD 1 ]---------------------------------------------------------------------------------------------------
pid   | 2588
state | idle in transaction
query | SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance +
      | FROM customer                                                                                           +
      | WHERE customer.id = 1 FOR UPDATE OF customer
-[ RECORD 2 ]---------------------------------------------------------------------------------------------------
pid   | 2613
state | active
query | UPDATE customer SET balance=111 WHERE customer.id = 1

datum=#

datum=# select * from customer;
-[ RECORD 1 ]-
id      | 1
name    | John
balance | 111

So we can see, first updated 222(by proc1) and then 111(by sec proc2)
datum=#
"""