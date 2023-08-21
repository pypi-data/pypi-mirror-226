import sys
"""

sys.path.append('/root/aafak/python-demo/package-import-exp/dir1/dir2')
import mod

#to avoid these things add file __init.py__ in all the dir
"""
from dir1.dir2 import mod as m
#or import dir1.dir2.mod as m
m.fun1()

"""
>>> ''.join([`x` for x in xrange(101)])
'0123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100'
>>> 
For example, we have the path like this, /home/k/TEST/PYTHON/p.py:

>>> os.path.dirname('/home/k/TEST/PYTHON/p.py')
'/home/k/TEST/PYTHON'

>>> os.path.basename('/home/k/TEST/PYTHON/p.py')
'p.py'

Or we can get them at once in tuple using os.path.split():

>>> os.path.split('/home/k/TEST/PYTHON/p.py')
('/home/k/TEST/PYTHON', 'p.py')

If we want to combine and make a full path:

>>> os.path.join('/home/k/TEST/PYTHON', 'p.py')
'/home/k/TEST/PYTHON/p.py'

"""
