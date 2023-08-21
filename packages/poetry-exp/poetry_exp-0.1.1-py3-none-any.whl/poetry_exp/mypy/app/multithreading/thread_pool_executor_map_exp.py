from concurrent.futures import ThreadPoolExecutor
from os import getpid
import  time


def worker(procnum):
    #print (greeting)
    print ('I am number %d in process %d' % (procnum, getpid()))
    return getpid()


def worker2(data):
    try:
        print(f'Processing data: {data}')
        time.sleep(5)
        if data['id'] == 2:
            raise ValueError("Invalid value")
        return {'result': {'status': True, "data": data}}
    except Exception as e:
        return {'result': {'status': False, "data": data, 'error': str(e)}}


if __name__ == '__main__':
    t1 = time.time()
    executor = ThreadPoolExecutor(max_workers=2)
    results = executor.map(worker2, [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}])
    for res in results:
        print(res)
    t2 = time.time()
    print(f'Time taken to process: {t2-t1} sec')

# 21.2 with 1 process
# 11.2 with 2 process
# 11.4 with 3 process
# 6.9 with 4 process
# In short , no of process will become a batch of task running parellely