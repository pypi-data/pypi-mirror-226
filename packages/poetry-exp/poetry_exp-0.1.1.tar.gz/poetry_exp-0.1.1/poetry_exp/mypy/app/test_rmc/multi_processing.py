import multiprocessing
import time
import copy
from main_dict import vcenter_cache_cls

def worker(di):
    """worker function"""
    print vcenter_cache_cls.main_dict
    if vcenter_cache_cls.main_dict:
        print 'refresinh...'
    else:
        print 'initilizing',
    d2 = {"newkey":"new_val"}
    print 'Worker'
    di['VM'] = "vm1"
    di['folder'] = {"name": "f1"}
    di['newDict'] = d2
    return

def worker2(di):
    """worker function"""
    print 'Worker2'
    di['datstore'] = "ds1"
    di['newDict2'] = {"newkey2": "new_val2"}
    return

def test():
    manager = multiprocessing.Manager()
    d = manager.dict()
    #d['u1'] = {}
    p1 = multiprocessing.Process(target=worker, args=(d,))
    p2 = multiprocessing.Process(target=worker2, args=(d,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print d
    #global main_dict
    vcenter_cache_cls.main_dict = d

    p1 = multiprocessing.Process(target=worker, args=(d,))
    p1.start()
    p1.join()


if __name__ == '__main__':
    test()
    print vcenter_cache_cls.main_dict
