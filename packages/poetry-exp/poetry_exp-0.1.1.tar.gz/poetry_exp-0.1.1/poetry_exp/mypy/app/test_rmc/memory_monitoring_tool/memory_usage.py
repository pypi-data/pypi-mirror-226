import os
import psutil
import time
import datetime
import sys
import logging
#from multiprocessing import Process, Manager
#from concurrent.futures import ProcessPoolExecutor

#executor = ProcessPoolExecutor(5)
# Gets or creates a logger
logger = logging.getLogger(__name__)

# set log level
logger.setLevel(logging.INFO)

# define file handler and set formatter
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s :: %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)

#logging.basicConfig(level=logging.INFO, file='memory_usage.log')
#logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
#logging.basicConfig(level=logging.INFO, format='%(asctime)s ::  %(message)s', file='memory_usage.log')


def memory_usage_psutil(pid):
    # return the memory usage in MB
    process = psutil.Process(pid)
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem


"""
Get the memory usage in MB
[root@rmc-jul24 aafak]# ps u -p 13410 | awk '{sum=sum+$6}; END {print sum/1024}'
63.4805
You have mail in /var/spool/mail/root
[root@rmc-jul24 aafak]#

"""
class HCache:
    cache = {}
    foo = []
    bar = []

def use_cache():
    cache_dict = HCache.cache
    a = cache_dict["vcenter"]["a"]
    b = cache_dict["vcenter"]["b"]
    c = cache_dict["vcenter"]["c"]
    d = cache_dict["vcenter"]["d"]
    e = cache_dict["vcenter"]["e"]
    f = cache_dict["vcenter"]["f"]
    g = cache_dict["vcenter"]["g"]
    h = cache_dict["vcenter"]["h"]
    i = cache_dict["vcenter"]["i"]
    j = cache_dict["vcenter"]["j"]
    k = cache_dict["vcenter"]["k"]
    m = cache_dict["vcenter"]["m"]
    n = cache_dict["vcenter"]["n"]
    o = cache_dict["vcenter"]["o"]
    p = cache_dict["vcenter"]["p"]
    #cache_dict[str(datetime.datetime.now())] = str(datetime.datetime.now())
    for k, v in cache_dict.items():
        f = cache_dict[k]

def get_folder(shared_dict):
    #print ("executing.....")
    shared_dict["q"] = ['q' * 10 ** 6]
    #print("executing.2....")
    shared_dict["r"] = ['r' * 10 ** 6]
    shared_dict["s"] = ['s' * 10 ** 6]
    shared_dict["t"] = ['t' * 10 ** 6]
    shared_dict["u"] = ['u' * 10 ** 6]
    shared_dict["v"] = ['v' * 10 ** 6]
    #print("executing...done..")
    #print(shared_dict)

def build_cache():
    cache_dict = HCache.cache
    shared_dict = dict() # Manager().dict()
    get_folder(shared_dict)
    #p = Process(target=get_folder, args=(shared_dict,))
    #p.start()
    #future = executor.submit(get_folder, shared_dict)
    cache_dict["vcenter"] = {}
    cache_dict["vcenter"]["a"] = ['a' * 10 ** 6]
    cache_dict["vcenter"]["b"] = ['b' * 10 ** 6]
    cache_dict["vcenter"]["c"] = ['c' * 10 ** 6]
    cache_dict["vcenter"]["d"] = ['d' * 10 ** 6]
    cache_dict["vcenter"]["e"] = ['e' * 10 ** 6]
    cache_dict["vcenter"]["f"] = ['f' * 10 ** 6]
    cache_dict["vcenter"]["g"] = ['g' * 10 ** 6]
    cache_dict["vcenter"]["h"] = ['h' * 10 ** 6]
    cache_dict["vcenter"]["i"] = ['i' * 10 ** 6]
    cache_dict["vcenter"]["j"] = ['j' * 10 ** 6]
    cache_dict["vcenter"]["k"] = ['k' * 10 ** 6]
    cache_dict["vcenter"]["k"] = ['l' * 10 ** 6]
    cache_dict["vcenter"]["m"] = ['m' * 10 ** 6]
    cache_dict["vcenter"]["n"] = ['n' * 10 ** 6]
    cache_dict["vcenter"]["o"] = ['o' * 10 ** 6]
    cache_dict["vcenter"]["p"] = ['p' * 10 ** 6]



    #p.join()
    #future.result()
    cache_dict["vcenter"]["q"] = shared_dict['q']
    cache_dict["vcenter"]["r"] = shared_dict['r']
    cache_dict["vcenter"]["s"] = shared_dict['s']
    cache_dict["vcenter"]["t"] = shared_dict['t']
    cache_dict["vcenter"]["u"] = shared_dict['u']
    cache_dict["vcenter"]["v"] = shared_dict['v']

def build_cache2():
    HCache.foo = ['bar' for _ in range(10000000)]
    HCache.bar = ['foo' for _ in range(10000000)]


def main():
    pid = os.getpid()
    # pid = int(sys.argv[1])
    count = 0
    while True:
        build_cache2()
        # use_cache()
        if count == 10:
            del HCache.foo
            del HCache.bar
            print('deleted')
            # pass
        count += 1
        mem_usage = memory_usage_psutil(pid)
        print("{0} {1} MB".format(datetime.datetime.now(), mem_usage))
        logger.info("{0} MB".format(mem_usage))
        time.sleep(2)

if __name__ == '__main__':
    main()


