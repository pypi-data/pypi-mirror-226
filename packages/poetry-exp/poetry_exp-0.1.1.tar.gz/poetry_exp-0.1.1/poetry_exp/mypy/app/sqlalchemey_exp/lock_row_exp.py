from sqlalchemy.orm import sessionmaker
import time
import os
from sqlalchemy import create_engine
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

# Run first time only
sm = sessionmaker()
sm.configure(bind=engine)
s = sm()
# Base.metadata.create_all(bind=engine)
#
# customers = [
#     Customer(name='John',
#          balance=0)
#     ]
# s.add_all(customers)
# s.commit()

customer = s.query(Customer).get(1)
print(f'[Main-Thread] Balance: {customer.balance} for customer id: {customer.id}')
customer.balance = 0
s.add(customer)
s.commit()
s.close()


def update_balance(thread_id):
    for i in range(1, 11):
        retry_count = 10
        count = 0
        while count <= retry_count:
            try:
                session = sm()
                customer = session.query(Customer).filter_by(id=1).with_for_update(of=Customer, nowait=True).one()
                print(f'[{thread_id}] Updating....->iteration:{i}')
                time.sleep(1)
                customer.balance = customer.balance + 1
                session.commit()
                session.flush(customer)
                print(f'[{thread_id}] Updated Balance: {customer.balance} ->iteration:{i}')
                session.close()
                break
            except OperationalError as e:
                print(f'[{thread_id}] Failed to get the row lock, retrying..')
                time.sleep(1)
                count += 1
            except Exception as e:
                print(f'[{thread_id}] Failed to update, retrying..')
                time.sleep(1)
                count += 1
        else:
            print(f'[{thread_id}] Failed to update for iteration: {i}')


if __name__ == '__main__':
    session1 = sm()
    # Following will lock the row until commit or rollback called
    customer = session1.query(Customer).filter_by(id=1).with_for_update(of=Customer, nowait=True).one()
    customer.balance = customer.balance + 1
    print(f'[Main-Thread] Updated the balance but not committed.....')
    session2 = sm()
    try:
       customer = session2.query(Customer).filter_by(id=1).with_for_update(of=Customer, nowait=True).one()
       customer.balance = customer.balance + 1
       session2.commit()
    except OperationalError as e:
        print(f'[Main-Thread] Failed to get the lock on row: {1}, error:{e}')
    session1.commit()
    session3 = sm()
    customer = session3.query(Customer).get(1)
    print(f'[Main-Thread] Balance: {customer.balance} for customer id: {customer.id}')

    threads = []
    for i in range(1, 6):
        th = Thread(target=update_balance, args=('Thread-'+str(i),))
        threads.append(th)
        th.start()

    for t in threads:
        t.join()

    session4 = sm()
    customer = session4.query(Customer).get(1)
    print(f'[Main-Thread] Final Balance: {customer.balance} for customer id: {customer.id}')



"""
# https://jaketrent.com/post/find-kill-locks-postgres
GET all the lock:
select pid, state, usename, query, query_start from pg_stat_activity;


datum=# select pid, mode, relname from pg_locks l join pg_class t on l.relation = t.oid and t.relkind = 'r' where t.relname = 'customer';
  pid  |        mode         | relname
-------+---------------------+----------
 27741 | RowShareLock        | customer
 27968 | AccessShareLock     | customer
 27968 | RowExclusiveLock    | customer
 27734 | RowShareLock        | customer
 29600 | AccessShareLock     | customer
 29600 | RowExclusiveLock    | customer
 27821 | AccessShareLock     | customer
 27821 | RowExclusiveLock    | customer
 27996 | AccessShareLock     | customer
 27996 | RowExclusiveLock    | customer
 27740 | RowShareLock        | customer
 27968 | ExclusiveLock       | customer
 27740 | AccessExclusiveLock | customer
 29600 | ExclusiveLock       | customer
 27996 | ExclusiveLock       | customer
 27734 | AccessExclusiveLock | customer
 27741 | AccessExclusiveLock | customer
(17 rows)


 select pid, state, usename, datname, wait_event, wait_event_type, query_start, query from pg_stat_activity where pid in (  select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');
-[ RECORD 1 ]---+---------------------------------------------------------------------------------------------------------
pid             | 27996
state           | active
usename         | datum
datname         | datum
wait_event      | tuple
wait_event_type | Lock
query_start     | 2022-08-23 02:43:55.275214+00
query           | UPDATE customer SET balance=111 WHERE customer.id = 1
-[ RECORD 2 ]---+---------------------------------------------------------------------------------------------------------
pid             | 27734
state           | active
usename         | datum
datname         | datum
wait_event      | tuple
wait_event_type | Lock
query_start     | 2022-08-23 02:43:17.438398+00
query           | SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance +
                | FROM customer                                                                                           +
                | WHERE customer.id = 1 FOR UPDATE OF customer
-[ RECORD 3 ]---+---------------------------------------------------------------------------------------------------------
pid             | 27740
state           | active
usename         | datum
datname         | datum
wait_event      | transactionid
wait_event_type | Lock
query_start     | 2022-08-23 02:42:17.365703+00
query           | SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance +
                | FROM customer                                                                                           +
                | WHERE customer.id = 1 FOR UPDATE OF customer
-[ RECORD 4 ]---+---------------------------------------------------------------------------------------------------------
pid             | 27741
state           | active
usename         | datum
datname         | datum
wait_event      | tuple
wait_event_type | Lock
query_start     | 2022-08-23 02:42:47.40038+00
query           | SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance +
                | FROM customer                                                                                           +
                | WHERE customer.id = 1 FOR UPDATE OF customer
-[ RECORD 5 ]---+---------------------------------------------------------------------------------------------------------
pid             | 27821
state           | idle in transaction
usename         | datum
datname         | datum
wait_event      | ClientRead
wait_event_type | Client
query_start     | 2022-08-23 02:41:46.083329+00
query           | UPDATE customer SET balance=111 WHERE customer.id = 1
-[ RECORD 6 ]---+---------------------------------------------------------------------------------------------------------
pid             | 27968
state           | active
usename         | datum
datname         | datum
wait_event      | tuple
wait_event_type | Lock
query_start     | 2022-08-23 02:43:32.029592+00
query           | UPDATE customer SET balance=111 WHERE customer.id = 1
-[ RECORD 7 ]---+---------------------------------------------------------------------------------------------------------
pid             | 29600
state           | active
usename         | datum
datname         | datum
wait_event      | tuple
wait_event_type | Lock
query_start     | 2022-08-23 03:00:45.986462+00
query           | UPDATE customer SET balance=111 WHERE customer.id = 1



Delete the locks:

datum=# select pg_cancel_backend(27996);    # Do this for all the active transaction
 pg_cancel_backend
-------------------
 t
(1 row)

datum=# select pid, state from pg_stat_activity where pid in (  select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');
  pid  |        state
-------+---------------------
 27821 | idle in transaction
(1 row)

datum=# select pg_cancel_backend(27821);   # Will not work for state (idle)
 pg_cancel_backend
-------------------
 t
(1 row)

datum=# select pid from pg_stat_activity where pid in (  select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');
  pid
-------
 27821
(1 row)

datum=#


datum=# select pg_terminate_backend(27821);
 pg_terminate_backend
----------------------
 t
(1 row)

datum=# select pid from pg_stat_activity where pid in (  select pid from pg_locks l join pg_class t on l.relation = t.oid  and t.relkind = 'r' where t.relname = 'customer');
 pid
-----
(0 rows)

datum=#



[root@Aafak-Local-CD-DO-May18 aafak]# python3 lock_row_exp.py
[Main-Thread] Balance: 21 for customer id: 1
[Main-Thread] Updated the balance but not committed.....
[Main-Thread] Failed to get the lock on row: 1, error:(psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8)
[Main-Thread] Balance: 1 for customer id: 1
[Thread-1] Updating....->iteration:1
[Thread-4] Failed to get the row lock, retrying..
[Thread-2] Failed to get the row lock, retrying..
[Thread-3] Failed to get the row lock, retrying..
[Thread-5] Failed to get the row lock, retrying..
[Thread-4] Failed to get the row lock, retrying..
[Thread-3] Failed to get the row lock, retrying..
[Thread-2] Failed to get the row lock, retrying..
[Thread-5] Failed to get the row lock, retrying..
[Thread-1] Updated Balance: 2 ->iteration:1
[Thread-1] Updating....->iteration:2
[Thread-4] Failed to get the row lock, retrying..
[Thread-2] Failed to get the row lock, retrying..
[Thread-5] Failed to get the row lock, retrying..
[Thread-3] Failed to get the row lock, retrying..
[Thread-1] Updated Balance: 3 ->iteration:2
[Thread-1] Updating....->iteration:3
[Thread-1] Updated Balance: 4 ->iteration:3
[Thread-1] Updating....->iteration:4
[Thread-1] Updated Balance: 5 ->iteration:4
[Thread-1] Updating....->iteration:5
[Thread-1] Updated Balance: 6 ->iteration:5
[Thread-1] Updating....->iteration:6
[Thread-1] Updated Balance: 7 ->iteration:6
[Thread-1] Updating....->iteration:7
[Thread-1] Updated Balance: 8 ->iteration:7
[Thread-1] Updating....->iteration:8
[Thread-1] Updated Balance: 9 ->iteration:8
[Thread-1] Updating....->iteration:9
[Thread-1] Updated Balance: 10 ->iteration:9
[Thread-1] Updating....->iteration:10
[Thread-1] Updated Balance: 11 ->iteration:10
[Thread-2] Updating....->iteration:1
[Thread-2] Updated Balance: 12 ->iteration:1
[Thread-2] Updating....->iteration:2
[Thread-2] Updated Balance: 13 ->iteration:2
[Thread-2] Updating....->iteration:3
[Thread-2] Updated Balance: 14 ->iteration:3
[Thread-2] Updating....->iteration:4
[Thread-2] Updated Balance: 15 ->iteration:4
[Thread-2] Updating....->iteration:5
[Thread-2] Updated Balance: 16 ->iteration:5
[Thread-2] Updating....->iteration:6
[Thread-2] Updated Balance: 17 ->iteration:6
[Thread-2] Updating....->iteration:7
[Thread-4] Failed to update, retrying..
[Thread-5] Failed to update, retrying..
[Thread-3] Failed to update, retrying..
[Thread-2] Updated Balance: 18 ->iteration:7
[Thread-2] Updating....->iteration:8
[Thread-2] Updated Balance: 19 ->iteration:8
[Thread-2] Updating....->iteration:9
[Thread-2] Updated Balance: 20 ->iteration:9
[Thread-2] Updating....->iteration:10
[Thread-2] Updated Balance: 21 ->iteration:10
[Thread-5] Updating....->iteration:1
[Thread-5] Updated Balance: 22 ->iteration:1
[Thread-5] Updating....->iteration:2
[Thread-5] Updated Balance: 23 ->iteration:2
[Thread-5] Updating....->iteration:3
[Thread-5] Updated Balance: 24 ->iteration:3
[Thread-5] Updating....->iteration:4
[Thread-5] Updated Balance: 25 ->iteration:4
[Thread-5] Updating....->iteration:5
[Thread-5] Updated Balance: 26 ->iteration:5
[Thread-5] Updating....->iteration:6
[Thread-5] Updated Balance: 27 ->iteration:6
[Thread-5] Updating....->iteration:7
[Thread-5] Updated Balance: 28 ->iteration:7
[Thread-5] Updating....->iteration:8
[Thread-5] Updated Balance: 29 ->iteration:8
[Thread-5] Updating....->iteration:9
[Thread-5] Updated Balance: 30 ->iteration:9
[Thread-5] Updating....->iteration:10
[Thread-5] Updated Balance: 31 ->iteration:10
[Thread-4] Updating....->iteration:1
[Thread-4] Updated Balance: 32 ->iteration:1
[Thread-4] Updating....->iteration:2
[Thread-3] Failed to update, retrying..
[Thread-4] Updated Balance: 33 ->iteration:2
[Thread-4] Updating....->iteration:3
[Thread-4] Updated Balance: 34 ->iteration:3
[Thread-4] Updating....->iteration:4
[Thread-4] Updated Balance: 35 ->iteration:4
[Thread-4] Updating....->iteration:5
[Thread-4] Updated Balance: 36 ->iteration:5
[Thread-4] Updating....->iteration:6
[Thread-4] Updated Balance: 37 ->iteration:6
[Thread-4] Updating....->iteration:7
[Thread-4] Updated Balance: 38 ->iteration:7
[Thread-4] Updating....->iteration:8
[Thread-4] Updated Balance: 39 ->iteration:8
[Thread-4] Updating....->iteration:9
[Thread-4] Updated Balance: 40 ->iteration:9
[Thread-4] Updating....->iteration:10
[Thread-4] Updated Balance: 41 ->iteration:10
[Thread-3] Updating....->iteration:1
[Thread-3] Updated Balance: 42 ->iteration:1
[Thread-3] Updating....->iteration:2
[Thread-3] Updated Balance: 43 ->iteration:2
[Thread-3] Updating....->iteration:3
[Thread-3] Updated Balance: 44 ->iteration:3
[Thread-3] Updating....->iteration:4
[Thread-3] Updated Balance: 45 ->iteration:4
[Thread-3] Updating....->iteration:5
[Thread-3] Updated Balance: 46 ->iteration:5
[Thread-3] Updating....->iteration:6
[Thread-3] Updated Balance: 47 ->iteration:6
[Thread-3] Updating....->iteration:7
[Thread-3] Updated Balance: 48 ->iteration:7
[Thread-3] Updating....->iteration:8
[Thread-3] Updated Balance: 49 ->iteration:8
[Thread-3] Updating....->iteration:9
[Thread-3] Updated Balance: 50 ->iteration:9
[Thread-3] Updating....->iteration:10
[Thread-3] Updated Balance: 51 ->iteration:10
[Main-Thread] Final Balance: 51 for customer id: 1
You have mail in /var/spool/mail/root
[root@Aafak-Local-CD-DO-May18 aafak]#


"""