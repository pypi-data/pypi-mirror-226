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
# engine = create_engine(DB_CONN_URL, pool_size=50, max_overflow=0)

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
print(f'[Main-Thread] [PID: {os.getpid()}] Balance: {customer.balance} for customer id: {customer.id}')


def update_balance(thread_id):
    for i in range(1, 11):
        retry_count = 10
        count = 0
        while count <= retry_count:
            try:
                session = sm()
                # Setting nowait=True will raise the exception immediately,
                # it will not wait for row lock to be released
                # no need to use it, without setting this, it worked well
                customer = session.query(Customer).filter_by(id=1).with_for_update(of=Customer, nowait=True).one()
                print(f'[PID: {os.getpid()}] [{thread_id}] Updating....->iteration:{i}')
                customer.balance = customer.balance + 1
                session.commit()
                session.flush(customer)
                print(f'[PID: {os.getpid()}] [{thread_id}] Updated Balance: {customer.balance} ->iteration:{i}')
                session.close()
                break
            except OperationalError as e:
                print(f'[PID: {os.getpid()}] [{thread_id}] Failed to get the row lock, error: {e} retrying..')
                time.sleep(1)
                count += 1
            except Exception as e:
                print(f'[PID: {os.getpid()}] [{thread_id}] Failed to update, error: {e}, retrying..')
                time.sleep(1)
                count += 1
        else:
            print(f'[PID: {os.getpid()}] [{thread_id}] Failed to update for iteration: {i}')


if __name__ == '__main__':
    # 5 Threads, each thread updating balance by 10,
    # running 1 instance of this script, will add 50
    # running 2 instance of this script, will make the final balance 100
    threads = []
    for i in range(1, 6):
        th = Thread(target=update_balance, args=('Thread-'+str(i),))
        threads.append(th)
        th.start()

    for t in threads:
        t.join()

    session4 = sm()
    customer = session4.query(Customer).get(1)
    print(f'[PID: {os.getpid()}] [Main-Thread] Final Balance: {customer.balance} for customer id: {customer.id}')



"""
datum=# update customer set balance=0;
UPDATE 1
datum=# select * from customer;
 id | name | balance
----+------+---------
  1 | John |       0
(1 row)

datum=#


@@@@@@@@@@@@@@@@@@@@@@@@@@@@Terminal -1 @@@@@@@@@@@@@@@@@@@@@@@@
[root@Aafak-Local-CD-DO-May18 aafak]# python3 thread_safe_update_multiple_process.py
[Main-Thread] [PID: 19111] Balance: 0 for customer id: 1
[PID: 19111] [Thread-2] Updating....->iteration:1
[PID: 19111] [Thread-1] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19111] [Thread-3] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19111] [Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..[PID: 19111] [Thread-5] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..

[PID: 19111] [Thread-2] Updated Balance: 1 ->iteration:1
[PID: 19111] [Thread-2] Updating....->iteration:2
[PID: 19111] [Thread-2] Updated Balance: 2 ->iteration:2
[PID: 19111] [Thread-2] Updating....->iteration:3
[PID: 19111] [Thread-2] Updated Balance: 3 ->iteration:3
[PID: 19111] [Thread-2] Updating....->iteration:4
[PID: 19111] [Thread-2] Updated Balance: 4 ->iteration:4
[PID: 19111] [Thread-2] Updating....->iteration:5
[PID: 19111] [Thread-2] Updated Balance: 5 ->iteration:5
[PID: 19111] [Thread-2] Updating....->iteration:6
[PID: 19111] [Thread-2] Updated Balance: 6 ->iteration:6
[PID: 19111] [Thread-2] Updating....->iteration:7
[PID: 19111] [Thread-2] Updated Balance: 7 ->iteration:7
[PID: 19111] [Thread-2] Updating....->iteration:8
[PID: 19111] [Thread-2] Updated Balance: 8 ->iteration:8
[PID: 19111] [Thread-2] Updating....->iteration:9
[PID: 19111] [Thread-2] Updated Balance: 9 ->iteration:9
[PID: 19111] [Thread-2] Updating....->iteration:10
[PID: 19111] [Thread-2] Updated Balance: 10 ->iteration:10
[PID: 19111] [Thread-1] Updating....->iteration:1
[PID: 19111] [Thread-3] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19111] [Thread-5] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19111] [Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19111] [Thread-1] Updated Balance: 11 ->iteration:1
[PID: 19111] [Thread-1] Updating....->iteration:2
[PID: 19111] [Thread-1] Updated Balance: 12 ->iteration:2
[PID: 19111] [Thread-1] Updating....->iteration:3
[PID: 19111] [Thread-1] Updated Balance: 13 ->iteration:3
[PID: 19111] [Thread-1] Updating....->iteration:4
[PID: 19111] [Thread-1] Updated Balance: 14 ->iteration:4
[PID: 19111] [Thread-1] Updating....->iteration:5
[PID: 19111] [Thread-1] Updated Balance: 15 ->iteration:5
[PID: 19111] [Thread-1] Updating....->iteration:6
[PID: 19111] [Thread-1] Updated Balance: 16 ->iteration:6
[PID: 19111] [Thread-1] Updating....->iteration:7
[PID: 19111] [Thread-1] Updated Balance: 17 ->iteration:7
[PID: 19111] [Thread-1] Updating....->iteration:8
[PID: 19111] [Thread-1] Updated Balance: 18 ->iteration:8
[PID: 19111] [Thread-1] Updating....->iteration:9
[PID: 19111] [Thread-1] Updated Balance: 19 ->iteration:9
[PID: 19111] [Thread-1] Updating....->iteration:10
[PID: 19111] [Thread-1] Updated Balance: 20 ->iteration:10
[PID: 19111] [Thread-3] Updating....->iteration:1
[PID: 19111] [Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19111] [Thread-5] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19111] [Thread-3] Updated Balance: 32 ->iteration:1
[PID: 19111] [Thread-3] Updating....->iteration:2
[PID: 19111] [Thread-3] Updated Balance: 33 ->iteration:2
[PID: 19111] [Thread-3] Updating....->iteration:3
[PID: 19111] [Thread-3] Updated Balance: 34 ->iteration:3
[PID: 19111] [Thread-3] Updating....->iteration:4
[PID: 19111] [Thread-3] Updated Balance: 35 ->iteration:4
[PID: 19111] [Thread-3] Updating....->iteration:5
[PID: 19111] [Thread-3] Updated Balance: 36 ->iteration:5
[PID: 19111] [Thread-3] Updating....->iteration:6
[PID: 19111] [Thread-3] Updated Balance: 37 ->iteration:6
[PID: 19111] [Thread-3] Updating....->iteration:7
[PID: 19111] [Thread-3] Updated Balance: 38 ->iteration:7
[PID: 19111] [Thread-3] Updating....->iteration:8
[PID: 19111] [Thread-3] Updated Balance: 39 ->iteration:8
[PID: 19111] [Thread-3] Updating....->iteration:9
[PID: 19111] [Thread-3] Updated Balance: 40 ->iteration:9
[PID: 19111] [Thread-3] Updating....->iteration:10
[PID: 19111] [Thread-3] Updated Balance: 41 ->iteration:10
[PID: 19111] [Thread-4] Updating....->iteration:1
[PID: 19111] [Thread-5] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19111] [Thread-4] Updated Balance: 52 ->iteration:1
[PID: 19111] [Thread-4] Updating....->iteration:2
[PID: 19111] [Thread-4] Updated Balance: 53 ->iteration:2
[PID: 19111] [Thread-4] Updating....->iteration:3
[PID: 19111] [Thread-4] Updated Balance: 54 ->iteration:3
[PID: 19111] [Thread-4] Updating....->iteration:4
[PID: 19111] [Thread-4] Updated Balance: 55 ->iteration:4
[PID: 19111] [Thread-4] Updating....->iteration:5
[PID: 19111] [Thread-4] Updated Balance: 56 ->iteration:5
[PID: 19111] [Thread-4] Updating....->iteration:6
[PID: 19111] [Thread-4] Updated Balance: 57 ->iteration:6
[PID: 19111] [Thread-4] Updating....->iteration:7
[PID: 19111] [Thread-4] Updated Balance: 58 ->iteration:7
[PID: 19111] [Thread-4] Updating....->iteration:8
[PID: 19111] [Thread-4] Updated Balance: 59 ->iteration:8
[PID: 19111] [Thread-4] Updating....->iteration:9
[PID: 19111] [Thread-4] Updated Balance: 60 ->iteration:9
[PID: 19111] [Thread-4] Updating....->iteration:10
[PID: 19111] [Thread-4] Updated Balance: 61 ->iteration:10
[PID: 19111] [Thread-5] Updating....->iteration:1
[PID: 19111] [Thread-5] Updated Balance: 72 ->iteration:1
[PID: 19111] [Thread-5] Updating....->iteration:2
[PID: 19111] [Thread-5] Updated Balance: 73 ->iteration:2
[PID: 19111] [Thread-5] Updating....->iteration:3
[PID: 19111] [Thread-5] Updated Balance: 74 ->iteration:3
[PID: 19111] [Thread-5] Updating....->iteration:4
[PID: 19111] [Thread-5] Updated Balance: 75 ->iteration:4
[PID: 19111] [Thread-5] Updating....->iteration:5
[PID: 19111] [Thread-5] Updated Balance: 76 ->iteration:5
[PID: 19111] [Thread-5] Updating....->iteration:6
[PID: 19111] [Thread-5] Updated Balance: 77 ->iteration:6
[PID: 19111] [Thread-5] Updating....->iteration:7
[PID: 19111] [Thread-5] Updated Balance: 78 ->iteration:7
[PID: 19111] [Thread-5] Updating....->iteration:8
[PID: 19111] [Thread-5] Updated Balance: 79 ->iteration:8
[PID: 19111] [Thread-5] Updating....->iteration:9
[PID: 19111] [Thread-5] Updated Balance: 80 ->iteration:9
[PID: 19111] [Thread-5] Updating....->iteration:10
[PID: 19111] [Thread-5] Updated Balance: 81 ->iteration:10
[PID: 19111] [Main-Thread] Final Balance: 81 for customer id: 1
[root@Aafak-Local-CD-DO-May18 aafak]#


********************************Terminal - 2 ************************
[root@Aafak-Local-CD-DO-May18 aafak]#  python3 thread_safe_update_multiple_process.py
[Main-Thread] [PID: 19127] Balance: 20 for customer id: 1
[PID: 19127] [Thread-2] Updating....->iteration:1
[PID: 19127] [Thread-1] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-3] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-2] Updated Balance: 21 ->iteration:1
[PID: 19127] [Thread-5] Updating....->iteration:1
[PID: 19127] [Thread-2] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-5] Updated Balance: 22 ->iteration:1
[PID: 19127] [Thread-5] Updating....->iteration:2
[PID: 19127] [Thread-5] Updated Balance: 23 ->iteration:2
[PID: 19127] [Thread-5] Updating....->iteration:3
[PID: 19127] [Thread-5] Updated Balance: 24 ->iteration:3
[PID: 19127] [Thread-5] Updating....->iteration:4
[PID: 19127] [Thread-5] Updated Balance: 25 ->iteration:4
[PID: 19127] [Thread-5] Updating....->iteration:5
[PID: 19127] [Thread-5] Updated Balance: 26 ->iteration:5
[PID: 19127] [Thread-5] Updating....->iteration:6
[PID: 19127] [Thread-5] Updated Balance: 27 ->iteration:6
[PID: 19127] [Thread-5] Updating....->iteration:7
[PID: 19127] [Thread-5] Updated Balance: 28 ->iteration:7
[PID: 19127] [Thread-5] Updating....->iteration:8
[PID: 19127] [Thread-5] Updated Balance: 29 ->iteration:8
[PID: 19127] [Thread-5] Updating....->iteration:9
[PID: 19127] [Thread-5] Updated Balance: 30 ->iteration:9
[PID: 19127] [Thread-5] Updating....->iteration:10
[PID: 19127] [Thread-5] Updated Balance: 31 ->iteration:10
[PID: 19127] [Thread-1] Updating....->iteration:1
[PID: 19127] [Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-3] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-1] Updated Balance: 42 ->iteration:1
[PID: 19127] [Thread-1] Updating....->iteration:2
[PID: 19127] [Thread-2] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-1] Updated Balance: 43 ->iteration:2
[PID: 19127] [Thread-1] Updating....->iteration:3
[PID: 19127] [Thread-1] Updated Balance: 44 ->iteration:3
[PID: 19127] [Thread-1] Updating....->iteration:4
[PID: 19127] [Thread-1] Updated Balance: 45 ->iteration:4
[PID: 19127] [Thread-1] Updating....->iteration:5
[PID: 19127] [Thread-1] Updated Balance: 46 ->iteration:5
[PID: 19127] [Thread-1] Updating....->iteration:6
[PID: 19127] [Thread-1] Updated Balance: 47 ->iteration:6
[PID: 19127] [Thread-1] Updating....->iteration:7
[PID: 19127] [Thread-1] Updated Balance: 48 ->iteration:7
[PID: 19127] [Thread-1] Updating....->iteration:8
[PID: 19127] [Thread-1] Updated Balance: 49 ->iteration:8
[PID: 19127] [Thread-1] Updating....->iteration:9
[PID: 19127] [Thread-1] Updated Balance: 50 ->iteration:9
[PID: 19127] [Thread-1] Updating....->iteration:10
[PID: 19127] [Thread-1] Updated Balance: 51 ->iteration:10
[PID: 19127] [Thread-4] Updating....->iteration:1
[PID: 19127] [Thread-3] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-4] Updated Balance: 62 ->iteration:1
[PID: 19127] [Thread-2] Updating....->iteration:2
[PID: 19127] [Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-2] Updated Balance: 63 ->iteration:2
[PID: 19127] [Thread-2] Updating....->iteration:3
[PID: 19127] [Thread-2] Updated Balance: 64 ->iteration:3
[PID: 19127] [Thread-2] Updating....->iteration:4
[PID: 19127] [Thread-2] Updated Balance: 65 ->iteration:4
[PID: 19127] [Thread-2] Updating....->iteration:5
[PID: 19127] [Thread-2] Updated Balance: 66 ->iteration:5
[PID: 19127] [Thread-2] Updating....->iteration:6
[PID: 19127] [Thread-2] Updated Balance: 67 ->iteration:6
[PID: 19127] [Thread-2] Updating....->iteration:7
[PID: 19127] [Thread-2] Updated Balance: 68 ->iteration:7
[PID: 19127] [Thread-2] Updating....->iteration:8
[PID: 19127] [Thread-2] Updated Balance: 69 ->iteration:8
[PID: 19127] [Thread-2] Updating....->iteration:9
[PID: 19127] [Thread-2] Updated Balance: 70 ->iteration:9
[PID: 19127] [Thread-2] Updating....->iteration:10
[PID: 19127] [Thread-2] Updated Balance: 71 ->iteration:10
[PID: 19127] [Thread-3] Updating....->iteration:1
[PID: 19127] [Thread-3] Updated Balance: 82 ->iteration:1
[PID: 19127] [Thread-3] Updating....->iteration:2
[PID: 19127] [Thread-4] Failed to get the row lock, error: (psycopg2.OperationalError) could not obtain lock on row in relation "customer"

[SQL: SELECT customer.id AS customer_id, customer.name AS customer_name, customer.balance AS customer_balance
FROM customer
WHERE customer.id = %(id_1)s FOR UPDATE OF customer NOWAIT]
[parameters: {'id_1': 1}]
(Background on this error at: http://sqlalche.me/e/e3q8) retrying..
[PID: 19127] [Thread-3] Updated Balance: 83 ->iteration:2
[PID: 19127] [Thread-3] Updating....->iteration:3
[PID: 19127] [Thread-3] Updated Balance: 84 ->iteration:3
[PID: 19127] [Thread-3] Updating....->iteration:4
[PID: 19127] [Thread-3] Updated Balance: 85 ->iteration:4
[PID: 19127] [Thread-3] Updating....->iteration:5
[PID: 19127] [Thread-3] Updated Balance: 86 ->iteration:5
[PID: 19127] [Thread-3] Updating....->iteration:6
[PID: 19127] [Thread-3] Updated Balance: 87 ->iteration:6
[PID: 19127] [Thread-3] Updating....->iteration:7
[PID: 19127] [Thread-3] Updated Balance: 88 ->iteration:7
[PID: 19127] [Thread-3] Updating....->iteration:8
[PID: 19127] [Thread-3] Updated Balance: 89 ->iteration:8
[PID: 19127] [Thread-3] Updating....->iteration:9
[PID: 19127] [Thread-3] Updated Balance: 90 ->iteration:9
[PID: 19127] [Thread-3] Updating....->iteration:10
[PID: 19127] [Thread-3] Updated Balance: 91 ->iteration:10
[PID: 19127] [Thread-4] Updating....->iteration:2
[PID: 19127] [Thread-4] Updated Balance: 92 ->iteration:2
[PID: 19127] [Thread-4] Updating....->iteration:3
[PID: 19127] [Thread-4] Updated Balance: 93 ->iteration:3
[PID: 19127] [Thread-4] Updating....->iteration:4
[PID: 19127] [Thread-4] Updated Balance: 94 ->iteration:4
[PID: 19127] [Thread-4] Updating....->iteration:5
[PID: 19127] [Thread-4] Updated Balance: 95 ->iteration:5
[PID: 19127] [Thread-4] Updating....->iteration:6
[PID: 19127] [Thread-4] Updated Balance: 96 ->iteration:6
[PID: 19127] [Thread-4] Updating....->iteration:7
[PID: 19127] [Thread-4] Updated Balance: 97 ->iteration:7
[PID: 19127] [Thread-4] Updating....->iteration:8
[PID: 19127] [Thread-4] Updated Balance: 98 ->iteration:8
[PID: 19127] [Thread-4] Updating....->iteration:9
[PID: 19127] [Thread-4] Updated Balance: 99 ->iteration:9
[PID: 19127] [Thread-4] Updating....->iteration:10
[PID: 19127] [Thread-4] Updated Balance: 100 ->iteration:10
[PID: 19127] [Main-Thread] Final Balance: 100 for customer id: 1
[root@Aafak-Local-CD-DO-May18 aafak]#


"""