# pip install python-memcached
import memcache
cache = memcache.Client(['127.0.0.1:11211'], debug=1)

# from werkzeug.contrib.cache import MemcachedCache
# cache = MemcachedCache(['127.0.0.1:1000'])

def get_users_from_db():
    print "Finding users from DB"
    return [
        {
            "name": "u1"
        },
        {
            "name": "u2"
        }

            ]

def get_users():
    users = cache.get('users')
    if users is None:
        users = get_users_from_db()
        cache.set("users", users, 60)

    return users


if __name__ == '__main__':

   for i in range(5):
       print get_users()

