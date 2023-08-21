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
                # This will lock the row and prevent
                # others to be update this row until this thread called the commit or rollback
                customer = session.query(Customer).filter_by(id=1).with_for_update(of=Customer).one()
                print(f'[PID: {os.getpid()}] [{thread_id}] Updating....->iteration:{i}')
                time.sleep(1)
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
datum=# select * from customer;
 id | name | balance
----+------+---------
  1 | John |     250
(1 row)

datum=#



@@@@@@@@@@@@@@@@@@@@@@@@@@@@Terminal -1 @@@@@@@@@@@@@@@@@@@@@@@@
[root@Aafak-Local-CD-DO-May18 aafak]# python3 thread_safe_update_multiple_process2.py
[Main-Thread] [PID: 20276] Balance: 250 for customer id: 1
[PID: 20276] [Thread-1] Updating....->iteration:1
[PID: 20276] [Thread-2] Updating....->iteration:1
[PID: 20276] [Thread-1] Updated Balance: 251 ->iteration:1
[PID: 20276] [Thread-4] Updating....->iteration:1
[PID: 20276] [Thread-2] Updated Balance: 252 ->iteration:1
[PID: 20276] [Thread-3] Updating....->iteration:1
[PID: 20276] [Thread-4] Updated Balance: 253 ->iteration:1
[PID: 20276] [Thread-5] Updating....->iteration:1
[PID: 20276] [Thread-3] Updated Balance: 254 ->iteration:1
[PID: 20276] [Thread-1] Updating....->iteration:2
[PID: 20276] [Thread-5] Updated Balance: 255 ->iteration:1
[PID: 20276] [Thread-1] Updated Balance: 256 ->iteration:2
[PID: 20276] [Thread-2] Updating....->iteration:2
[PID: 20276] [Thread-2] Updated Balance: 259 ->iteration:2
[PID: 20276] [Thread-4] Updating....->iteration:2
[PID: 20276] [Thread-4] Updated Balance: 262 ->iteration:2
[PID: 20276] [Thread-3] Updating....->iteration:2
[PID: 20276] [Thread-5] Updating....->iteration:2
[PID: 20276] [Thread-3] Updated Balance: 264 ->iteration:2
[PID: 20276] [Thread-1] Updating....->iteration:3
[PID: 20276] [Thread-5] Updated Balance: 265 ->iteration:2
[PID: 20276] [Thread-1] Updated Balance: 266 ->iteration:3
[PID: 20276] [Thread-2] Updating....->iteration:3
[PID: 20276] [Thread-2] Updated Balance: 268 ->iteration:3
[PID: 20276] [Thread-4] Updating....->iteration:3
[PID: 20276] [Thread-4] Updated Balance: 271 ->iteration:3
[PID: 20276] [Thread-3] Updating....->iteration:3
[PID: 20276] [Thread-5] Updating....->iteration:3
[PID: 20276] [Thread-3] Updated Balance: 273 ->iteration:3
[PID: 20276] [Thread-1] Updating....->iteration:4
[PID: 20276] [Thread-5] Updated Balance: 274 ->iteration:3
[PID: 20276] [Thread-1] Updated Balance: 275 ->iteration:4
[PID: 20276] [Thread-2] Updating....->iteration:4
[PID: 20276] [Thread-2] Updated Balance: 277 ->iteration:4
[PID: 20276] [Thread-3] Updating....->iteration:4
[PID: 20276] [Thread-5] Updating....->iteration:4
[PID: 20276] [Thread-3] Updated Balance: 281 ->iteration:4
[PID: 20276] [Thread-4] Updating....->iteration:4
[PID: 20276] [Thread-5] Updated Balance: 282 ->iteration:4
[PID: 20276] [Thread-1] Updating....->iteration:5
[PID: 20276] [Thread-4] Updated Balance: 283 ->iteration:4
[PID: 20276] [Thread-1] Updated Balance: 284 ->iteration:5
[PID: 20276] [Thread-2] Updating....->iteration:5
[PID: 20276] [Thread-2] Updated Balance: 287 ->iteration:5
[PID: 20276] [Thread-3] Updating....->iteration:5
[PID: 20276] [Thread-5] Updating....->iteration:5
[PID: 20276] [Thread-3] Updated Balance: 290 ->iteration:5
[PID: 20276] [Thread-4] Updating....->iteration:5
[PID: 20276] [Thread-5] Updated Balance: 291 ->iteration:5
[PID: 20276] [Thread-4] Updated Balance: 292 ->iteration:5
[PID: 20276] [Thread-1] Updating....->iteration:6
[PID: 20276] [Thread-3] Updating....->iteration:6
[PID: 20276] [Thread-1] Updated Balance: 295 ->iteration:6
[PID: 20276] [Thread-3] Updated Balance: 296 ->iteration:6
[PID: 20276] [Thread-2] Updating....->iteration:6
[PID: 20276] [Thread-2] Updated Balance: 298 ->iteration:6
[PID: 20276] [Thread-4] Updating....->iteration:6
[PID: 20276] [Thread-5] Updating....->iteration:6
[PID: 20276] [Thread-4] Updated Balance: 301 ->iteration:6
[PID: 20276] [Thread-3] Updating....->iteration:7
[PID: 20276] [Thread-5] Updated Balance: 302 ->iteration:6
[PID: 20276] [Thread-1] Updating....->iteration:7
[PID: 20276] [Thread-3] Updated Balance: 303 ->iteration:7
[PID: 20276] [Thread-1] Updated Balance: 304 ->iteration:7
[PID: 20276] [Thread-2] Updating....->iteration:7
[PID: 20276] [Thread-2] Updated Balance: 307 ->iteration:7
[PID: 20276] [Thread-3] Updating....->iteration:8
[PID: 20276] [Thread-3] Updated Balance: 309 ->iteration:8
[PID: 20276] [Thread-4] Updating....->iteration:7
[PID: 20276] [Thread-5] Updating....->iteration:7
[PID: 20276] [Thread-4] Updated Balance: 311 ->iteration:7
[PID: 20276] [Thread-5] Updated Balance: 312 ->iteration:7
[PID: 20276] [Thread-1] Updating....->iteration:8
[PID: 20276] [Thread-2] Updating....->iteration:8
[PID: 20276] [Thread-1] Updated Balance: 316 ->iteration:8
[PID: 20276] [Thread-2] Updated Balance: 317 ->iteration:8
[PID: 20276] [Thread-3] Updating....->iteration:9
[PID: 20276] [Thread-3] Updated Balance: 319 ->iteration:9
[PID: 20276] [Thread-4] Updating....->iteration:8
[PID: 20276] [Thread-4] Updated Balance: 321 ->iteration:8
[PID: 20276] [Thread-5] Updating....->iteration:8
[PID: 20276] [Thread-1] Updating....->iteration:9
[PID: 20276] [Thread-5] Updated Balance: 324 ->iteration:8
[PID: 20276] [Thread-1] Updated Balance: 325 ->iteration:9
[PID: 20276] [Thread-2] Updating....->iteration:9
[PID: 20276] [Thread-2] Updated Balance: 327 ->iteration:9
[PID: 20276] [Thread-3] Updating....->iteration:10
[PID: 20276] [Thread-3] Updated Balance: 329 ->iteration:10
[PID: 20276] [Thread-4] Updating....->iteration:9
[PID: 20276] [Thread-4] Updated Balance: 331 ->iteration:9
[PID: 20276] [Thread-5] Updating....->iteration:9
[PID: 20276] [Thread-1] Updating....->iteration:10
[PID: 20276] [Thread-5] Updated Balance: 334 ->iteration:9
[PID: 20276] [Thread-1] Updated Balance: 335 ->iteration:10
[PID: 20276] [Thread-4] Updating....->iteration:10
[PID: 20276] [Thread-4] Updated Balance: 339 ->iteration:10
[PID: 20276] [Thread-5] Updating....->iteration:10
[PID: 20276] [Thread-5] Updated Balance: 341 ->iteration:10
[PID: 20276] [Thread-2] Updating....->iteration:10
[PID: 20276] [Thread-2] Updated Balance: 347 ->iteration:10
[PID: 20276] [Main-Thread] Final Balance: 347 for customer id: 1
You have mail in /var/spool/mail/root
[root@Aafak-Local-CD-DO-May18 aafak]#


********************************Terminal - 2 ************************
[root@Aafak-Local-CD-DO-May18 aafak]#  python3 thread_safe_update_multiple_process2.py
[Main-Thread] [PID: 20290] Balance: 251 for customer id: 1
[PID: 20290] [Thread-1] Updating....->iteration:1
[PID: 20290] [Thread-3] Updating....->iteration:1
[PID: 20290] [Thread-1] Updated Balance: 257 ->iteration:1
[PID: 20290] [Thread-3] Updated Balance: 258 ->iteration:1
[PID: 20290] [Thread-4] Updating....->iteration:1
[PID: 20290] [Thread-2] Updating....->iteration:1
[PID: 20290] [Thread-4] Updated Balance: 260 ->iteration:1
[PID: 20290] [Thread-2] Updated Balance: 261 ->iteration:1
[PID: 20290] [Thread-5] Updating....->iteration:1
[PID: 20290] [Thread-5] Updated Balance: 263 ->iteration:1
[PID: 20290] [Thread-3] Updating....->iteration:2
[PID: 20290] [Thread-3] Updated Balance: 267 ->iteration:2
[PID: 20290] [Thread-4] Updating....->iteration:2
[PID: 20290] [Thread-2] Updating....->iteration:2
[PID: 20290] [Thread-4] Updated Balance: 269 ->iteration:2
[PID: 20290] [Thread-2] Updated Balance: 270 ->iteration:2
[PID: 20290] [Thread-5] Updating....->iteration:2
[PID: 20290] [Thread-5] Updated Balance: 272 ->iteration:2
[PID: 20290] [Thread-3] Updating....->iteration:3
[PID: 20290] [Thread-3] Updated Balance: 276 ->iteration:3
[PID: 20290] [Thread-4] Updating....->iteration:3
[PID: 20290] [Thread-2] Updating....->iteration:3
[PID: 20290] [Thread-4] Updated Balance: 278 ->iteration:3
[PID: 20290] [Thread-5] Updating....->iteration:3
[PID: 20290] [Thread-2] Updated Balance: 279 ->iteration:3
[PID: 20290] [Thread-5] Updated Balance: 280 ->iteration:3
[PID: 20290] [Thread-1] Updating....->iteration:2
[PID: 20290] [Thread-3] Updating....->iteration:4
[PID: 20290] [Thread-1] Updated Balance: 285 ->iteration:2
[PID: 20290] [Thread-3] Updated Balance: 286 ->iteration:4
[PID: 20290] [Thread-4] Updating....->iteration:4
[PID: 20290] [Thread-5] Updating....->iteration:4
[PID: 20290] [Thread-4] Updated Balance: 288 ->iteration:4
[PID: 20290] [Thread-5] Updated Balance: 289 ->iteration:4
[PID: 20290] [Thread-2] Updating....->iteration:4
[PID: 20290] [Thread-4] Updating....->iteration:5
[PID: 20290] [Thread-2] Updated Balance: 293 ->iteration:4
[PID: 20290] [Thread-4] Updated Balance: 294 ->iteration:5
[PID: 20290] [Thread-5] Updating....->iteration:5
[PID: 20290] [Thread-5] Updated Balance: 297 ->iteration:5
[PID: 20290] [Thread-3] Updating....->iteration:5
[PID: 20290] [Thread-4] Updating....->iteration:6
[PID: 20290] [Thread-3] Updated Balance: 299 ->iteration:5
[PID: 20290] [Thread-4] Updated Balance: 300 ->iteration:6
[PID: 20290] [Thread-5] Updating....->iteration:6
[PID: 20290] [Thread-1] Updating....->iteration:3
[PID: 20290] [Thread-5] Updated Balance: 305 ->iteration:6
[PID: 20290] [Thread-1] Updated Balance: 306 ->iteration:3
[PID: 20290] [Thread-4] Updating....->iteration:7
[PID: 20290] [Thread-4] Updated Balance: 308 ->iteration:7
[PID: 20290] [Thread-3] Updating....->iteration:6
[PID: 20290] [Thread-3] Updated Balance: 310 ->iteration:6
[PID: 20290] [Thread-2] Updating....->iteration:5
[PID: 20290] [Thread-4] Updating....->iteration:8
[PID: 20290] [Thread-2] Updated Balance: 313 ->iteration:5
[PID: 20290] [Thread-5] Updating....->iteration:7
[PID: 20290] [Thread-4] Updated Balance: 314 ->iteration:8
[PID: 20290] [Thread-5] Updated Balance: 315 ->iteration:7
[PID: 20290] [Thread-1] Updating....->iteration:4
[PID: 20290] [Thread-1] Updated Balance: 318 ->iteration:4
[PID: 20290] [Thread-3] Updating....->iteration:7
[PID: 20290] [Thread-3] Updated Balance: 320 ->iteration:7
[PID: 20290] [Thread-5] Updating....->iteration:8
[PID: 20290] [Thread-4] Updating....->iteration:9
[PID: 20290] [Thread-5] Updated Balance: 322 ->iteration:8
[PID: 20290] [Thread-4] Updated Balance: 323 ->iteration:9
[PID: 20290] [Thread-2] Updating....->iteration:6
[PID: 20290] [Thread-2] Updated Balance: 326 ->iteration:6
[PID: 20290] [Thread-5] Updating....->iteration:9
[PID: 20290] [Thread-5] Updated Balance: 328 ->iteration:9
[PID: 20290] [Thread-1] Updating....->iteration:5
[PID: 20290] [Thread-1] Updated Balance: 330 ->iteration:5
[PID: 20290] [Thread-4] Updating....->iteration:10
[PID: 20290] [Thread-3] Updating....->iteration:8
[PID: 20290] [Thread-4] Updated Balance: 332 ->iteration:10
[PID: 20290] [Thread-3] Updated Balance: 333 ->iteration:8
[PID: 20290] [Thread-2] Updating....->iteration:7
[PID: 20290] [Thread-5] Updating....->iteration:10
[PID: 20290] [Thread-2] Updated Balance: 336 ->iteration:7
[PID: 20290] [Thread-1] Updating....->iteration:6
[PID: 20290] [Thread-5] Updated Balance: 337 ->iteration:10
[PID: 20290] [Thread-1] Updated Balance: 338 ->iteration:6
[PID: 20290] [Thread-3] Updating....->iteration:9
[PID: 20290] [Thread-3] Updated Balance: 340 ->iteration:9
[PID: 20290] [Thread-2] Updating....->iteration:8
[PID: 20290] [Thread-1] Updating....->iteration:7
[PID: 20290] [Thread-2] Updated Balance: 342 ->iteration:8
[PID: 20290] [Thread-3] Updating....->iteration:10
[PID: 20290] [Thread-1] Updated Balance: 343 ->iteration:7
[PID: 20290] [Thread-2] Updating....->iteration:9
[PID: 20290] [Thread-3] Updated Balance: 344 ->iteration:10
[PID: 20290] [Thread-1] Updating....->iteration:8
[PID: 20290] [Thread-2] Updated Balance: 345 ->iteration:9
[PID: 20290] [Thread-1] Updated Balance: 346 ->iteration:8
[PID: 20290] [Thread-2] Updating....->iteration:10
[PID: 20290] [Thread-1] Updating....->iteration:9
[PID: 20290] [Thread-2] Updated Balance: 348 ->iteration:10
[PID: 20290] [Thread-1] Updated Balance: 349 ->iteration:9
[PID: 20290] [Thread-1] Updating....->iteration:10
[PID: 20290] [Thread-1] Updated Balance: 350 ->iteration:10
[PID: 20290] [Main-Thread] Final Balance: 350 for customer id: 1
You have mail in /var/spool/mail/root
[root@Aafak-Local-CD-DO-May18 aafak]#


"""