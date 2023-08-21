# https://myedukit.com/coders/python-examples/sqlalchemy-lock-row/

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


def update_balance(thread_id):
    for i in range(1, 11):
        retry_count = 10
        count = 0
        while count <= retry_count:
            try:
                session = sm()
                # Don't use this flag nowait=True,
                # then no need of this retry, it will wait for lock to be released
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
                print(f'[{thread_id}] Failed to get the row lock, error: {e} retrying..')
                time.sleep(1)
                count += 1
            except Exception as e:
                print(f'[{thread_id}] Failed to update, error: {e}, retrying..')
                time.sleep(1)
                count += 1
        else:
            print(f'[{thread_id}] Failed to update for iteration: {i}')


if __name__ == '__main__':

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
datum=# update customer set balance=0;
UPDATE 1
datum=# select * from customer;
 id | name | balance
----+------+---------
  1 | John |       0
(1 row)

datum=#


[root@Aafak-Local-CD-DO-May18 aafak]# python3 thread_safe_update.py
[Main-Thread] Balance: 0 for customer id: 1
[Thread-1] Updating....->iteration:1
[Thread-2] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-3] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-5] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-2] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-3] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-5] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..[Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..

[Thread-1] Updated Balance: 1 ->iteration:1
[Thread-1] Updating....->iteration:2
[Thread-2] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-3] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-5] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-2] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[Thread-1] Updated Balance: 2 ->iteration:2
[Thread-1] Updating....->iteration:3
[Thread-1] Updated Balance: 3 ->iteration:3
[Thread-1] Updating....->iteration:4
[Thread-1] Updated Balance: 4 ->iteration:4
[Thread-1] Updating....->iteration:5
[Thread-1] Updated Balance: 5 ->iteration:5
[Thread-1] Updating....->iteration:6
[Thread-1] Updated Balance: 6 ->iteration:6
[Thread-1] Updating....->iteration:7
[Thread-1] Updated Balance: 7 ->iteration:7
[Thread-1] Updating....->iteration:8
[Thread-1] Updated Balance: 8 ->iteration:8
[Thread-1] Updating....->iteration:9
[Thread-1] Updated Balance: 9 ->iteration:9
[Thread-1] Updating....->iteration:10
[Thread-1] Updated Balance: 10 ->iteration:10
[Thread-2] Updating....->iteration:1
[Thread-2] Updated Balance: 11 ->iteration:1
[Thread-2] Updating....->iteration:2
[Thread-2] Updated Balance: 12 ->iteration:2
[Thread-2] Updating....->iteration:3
[Thread-2] Updated Balance: 13 ->iteration:3
[Thread-2] Updating....->iteration:4
[Thread-2] Updated Balance: 14 ->iteration:4
[Thread-2] Updating....->iteration:5
[Thread-2] Updated Balance: 15 ->iteration:5
[Thread-2] Updating....->iteration:6
[Thread-2] Updated Balance: 16 ->iteration:6
[Thread-2] Updating....->iteration:7
[Thread-3] Failed to update, error: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30 (Background on this error at: http://sqlalche.me/e/3o7r), retrying..
[Thread-5] Failed to update, error: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30 (Background on this error at: http://sqlalche.me/e/3o7r), retrying..
[Thread-4] Failed to update, error: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30 (Background on this error at: http://sqlalche.me/e/3o7r), retrying..
[Thread-2] Updated Balance: 17 ->iteration:7
[Thread-2] Updating....->iteration:8
[Thread-2] Updated Balance: 18 ->iteration:8
[Thread-2] Updating....->iteration:9
[Thread-2] Updated Balance: 19 ->iteration:9
[Thread-2] Updating....->iteration:10
[Thread-2] Updated Balance: 20 ->iteration:10
[Thread-5] Updating....->iteration:1
[Thread-5] Updated Balance: 21 ->iteration:1
[Thread-5] Updating....->iteration:2
[Thread-5] Updated Balance: 22 ->iteration:2
[Thread-5] Updating....->iteration:3
[Thread-5] Updated Balance: 23 ->iteration:3
[Thread-5] Updating....->iteration:4
[Thread-5] Updated Balance: 24 ->iteration:4
[Thread-5] Updating....->iteration:5
[Thread-5] Updated Balance: 25 ->iteration:5
[Thread-5] Updating....->iteration:6
[Thread-5] Updated Balance: 26 ->iteration:6
[Thread-5] Updating....->iteration:7
[Thread-5] Updated Balance: 27 ->iteration:7
[Thread-5] Updating....->iteration:8
[Thread-5] Updated Balance: 28 ->iteration:8
[Thread-5] Updating....->iteration:9
[Thread-5] Updated Balance: 29 ->iteration:9
[Thread-5] Updating....->iteration:10
[Thread-5] Updated Balance: 30 ->iteration:10
[Thread-3] Updating....->iteration:1
[Thread-3] Updated Balance: 31 ->iteration:1
[Thread-3] Updating....->iteration:2
[Thread-4] Failed to update, error: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30 (Background on this error at: http://sqlalche.me/e/3o7r), retrying..
[Thread-3] Updated Balance: 32 ->iteration:2
[Thread-3] Updating....->iteration:3
[Thread-3] Updated Balance: 33 ->iteration:3
[Thread-3] Updating....->iteration:4
[Thread-3] Updated Balance: 34 ->iteration:4
[Thread-3] Updating....->iteration:5
[Thread-3] Updated Balance: 35 ->iteration:5
[Thread-3] Updating....->iteration:6
[Thread-3] Updated Balance: 36 ->iteration:6
[Thread-3] Updating....->iteration:7
[Thread-3] Updated Balance: 37 ->iteration:7
[Thread-3] Updating....->iteration:8
[Thread-3] Updated Balance: 38 ->iteration:8
[Thread-3] Updating....->iteration:9
[Thread-3] Updated Balance: 39 ->iteration:9
[Thread-3] Updating....->iteration:10
[Thread-3] Updated Balance: 40 ->iteration:10
[Thread-4] Updating....->iteration:1
[Thread-4] Updated Balance: 41 ->iteration:1
[Thread-4] Updating....->iteration:2
[Thread-4] Updated Balance: 42 ->iteration:2
[Thread-4] Updating....->iteration:3
[Thread-4] Updated Balance: 43 ->iteration:3
[Thread-4] Updating....->iteration:4
[Thread-4] Updated Balance: 44 ->iteration:4
[Thread-4] Updating....->iteration:5
[Thread-4] Updated Balance: 45 ->iteration:5
[Thread-4] Updating....->iteration:6
[Thread-4] Updated Balance: 46 ->iteration:6
[Thread-4] Updating....->iteration:7
[Thread-4] Updated Balance: 47 ->iteration:7
[Thread-4] Updating....->iteration:8
[Thread-4] Updated Balance: 48 ->iteration:8
[Thread-4] Updating....->iteration:9
[Thread-4] Updated Balance: 49 ->iteration:9
[Thread-4] Updating....->iteration:10
[Thread-4] Updated Balance: 50 ->iteration:10
[Main-Thread] Final Balance: 50 for customer id: 1
You have mail in /var/spool/mail/root
[root@Aafak-Local-CD-DO-May18 aafak]#


"""