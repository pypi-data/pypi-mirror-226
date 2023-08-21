import redis

redis_client = redis.Redis(host='localhost', port='6379')

redis_client.delete('bkpLockForResource')
redis_client.delete('snapLockForResource')
redis_client.delete('__bkp__res-uuid-1')

key_added = redis_client.set('bkpLockForResource', 'res1')
print(key_added)  # True

key_added = redis_client.set('bkpLockForResource', 'res2')   # will overwrite
print(key_added)  # True
print(redis_client.get('bkpLockForResource'))  # b'res2'


key_added = redis_client.set('snapLockForResource', 'res1', nx=True)  # nx: add only if not exit
print(key_added)  # True

key_added = redis_client.set('snapLockForResource', 'res2', nx=True)  # will not overwrite
print(key_added)  # None
print(redis_client.get('snapLockForResource'))  # b'res1'

redis_client.delete('bkpLockForResource')
redis_client.delete('snapLockForResource')
redis_client.delete('__bkp__res-uuid-1')

"""
True
True
b'res2'
True
None
b'res1'
"""