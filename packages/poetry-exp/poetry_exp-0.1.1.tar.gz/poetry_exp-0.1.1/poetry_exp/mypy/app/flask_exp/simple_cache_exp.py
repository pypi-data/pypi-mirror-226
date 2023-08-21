
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()  # its working

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
        cache.set("users", users, timeout=5*60)

    return users


if __name__ == '__main__':

   for i in range(5):
       print get_users()


"""
OUTPUT:
Finding users from DB
[{'name': 'u1'}, {'name': 'u2'}]
[{'name': 'u1'}, {'name': 'u2'}]
[{'name': 'u1'}, {'name': 'u2'}]
[{'name': 'u1'}, {'name': 'u2'}]
[{'name': 'u1'}, {'name': 'u2'}]
"""