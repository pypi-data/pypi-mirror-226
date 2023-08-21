import memcache
import bmemcached
from datetime import datetime

# ("127.0.0.1:11211",)
memcache_client = memcache.Memcache(("127.0.0.1", 11211))

memcache_client.delete('bkpLockForResource')
memcache_client.delete('snapLockForResource')
memcache_client.delete('bkpLockForResource2')
memcache_client.delete('snapLockForResource2')

key_added = memcache_client.set('bkpLockForResource', 'res1')
print(key_added)  # True

key_added = memcache_client.set('bkpLockForResource', 'res2')   # will overwrite
print(key_added)  # True
print(memcache_client.get('bkpLockForResource'))  # b'res2'


key_added = memcache_client.set('snapLockForResource', 'res1')
print(key_added)  # True

key_added = memcache_client.set('snapLockForResource', 'res2')  # will overwrite
print(key_added)  # None
print(memcache_client.get('snapLockForResource'))  # b'res1'


print(f'Using bmemcached')
# Using bmemcached
memcache_client = bmemcached.Client(('127.0.0.1:11211', ))
key_added = memcache_client.add('bkpLockForResource2', 'res1')
print(key_added)  # True

key_added = memcache_client.add('bkpLockForResource2', 'res2')   # will not overwrite
print(key_added)  # False
print(memcache_client.get('bkpLockForResource2'))  # b'res1'

key_added = memcache_client.add('snapLockForResource2', 'res1')
print(key_added)  # True

key_added = memcache_client.add('snapLockForResource2', 'res2')  # will not overwrite
print(key_added)  # False
print(memcache_client.get('snapLockForResource2'))  # b'res1'

memcache_client.delete('bkpLockForResource')
memcache_client.delete('snapLockForResource')
memcache_client.delete('bkpLockForResource2')
memcache_client.delete('snapLockForResource2')
memcache_client.delete('__bkp__res-uuid-1')

"""
None
None
res2
None
None
res2
Using bmemcached
True
False
res1
True
False
res1
"""