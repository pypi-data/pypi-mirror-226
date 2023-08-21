import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

def worker():
    logging.debug('Starting')
    time.sleep(2)
    logging.debug('Exiting')

def my_service():
    logging.debug('Starting')
    time.sleep(3)
    logging.debug('Exiting')

def ha_thread1(nodeId):
  logging.error("HA thread1 starting....nodeId: "+nodeId)
  time.sleep(5)
  logging.error("HA thread1 completed")

t = threading.Thread(name='my_service', target=my_service)
w = threading.Thread(name='worker', target=worker)
w2 = threading.Thread(target=worker) # use default name
haThread1 = threading.Thread(name="HA Thread1", target=ha_thread1, args=("f8c7c7bc-daf1-3cfb-a9d8-72912ae63373",))
haThread1.start()
w.start()
w2.start()
t.start()

logging.info("Main thread exited")

