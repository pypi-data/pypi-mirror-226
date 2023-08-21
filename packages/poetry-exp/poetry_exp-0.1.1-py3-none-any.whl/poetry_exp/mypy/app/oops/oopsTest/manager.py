import os
import sys
sys.path.append('/root/aafak/python-demo/python-program/oops')
import poolutils

"""sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 
os.pardir, os.pardir)))"""

poolConfig=poolutils.PoolConfiguration()



poolConfig.createStoragePool(5)
