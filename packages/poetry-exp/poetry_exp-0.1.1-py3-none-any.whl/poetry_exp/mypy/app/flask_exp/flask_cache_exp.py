# https://pythonhosted.org/Flask-Cache/
# pip install Flask-Cache
"""
index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>Title</title>
</head>
<body>
Hell this is cacheingfghghggjg hjhj fgghjghj
  <img src="{{url_for('static', filename='IOT_ref_arch.png')}}" />

</body>
</html>


"""
from flask import Flask, render_template, json, make_response
from flask_caching import Cache
import time

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_THRESHOLD':15, 'CACHE_DEFAULT_TIMEOUT': 5*60})
#cache = Cache(app, config={'CACHE_TYPE': 'memcached', 'CACHE_DEFAULT_TIMEOUT': 2})

"""
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'fcache',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://localhost:6379'
    })
#url = redis://user:password@localhost:6379/2    
"""
#cache.init_app(app)

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


@app.route("/")
#@cache.cached()  # this must be here, changing the order will not cache the result
def index():
    print "executing request..."
    response = make_response(render_template("index.html"))
    #print dir(response)
    # request will come every time here but, the images used in index.html will be cached by browser
    # You can check this in chrome network tab in size column it will say(from memory cached for the images) from second request onwords
    # it will send a unique e-tag and Cache-Control info in response header
    # Next time browser will send request with header containing attribute If-None-Match: with same e-tag
    response.headers['Cache-Control'] = "max-age=5, public" # one hour 3600
    #time.sleep(1)
    return response

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
# response.headers['Cache-Control'] = "max-age=5, private" # specific to a person
# response.headers['Cache-Control'] = "max-age=5, no-store" # indicate that it should never be cached
# what to cache: image, css, js

# To turn off caching: Cache-Control: no-cache, no-store, must-revalidate
# Caching static assets: Cache-Control: public, max-age=31536000
#

@app.route("/users/<id>")
@cache.cached(timeout=5*60)  # override the config timout value for this method
def users(id):  # will not cache the arguments
    print "executing request...user: ", id
    return json.dumps(get_users_from_db())

@app.route("/products/<id>")
@cache.memoize(50)  # override the config timout value for this method
def products(id):  # will not cache the arguments
    print "executing request for finding product: ", id
    return json.dumps(get_users_from_db())

#With functions that do not receive arguments, cached() and memoize() are effectively the same.

class Item(object):
    def __init__(self, item_id=0):
        self.item_id = item_id

    @cache.memoize(timeout=5*60)
    def find_item(self): # memoize will consider the identity of object
        print "item object: ", self
        print "Finding item: ", self.item_id
        return [{"item_id":self.item_id}]

#i = Item()

@app.route("/items/<id>")
def items(id):
    #i.item_id = id
    i = Item(id)
    return json.dumps(i.find_item())

if __name__ == '__main__':
    app.run(debug=True)


"""
Request Directive:
Cache-Control: max-age=<seconds>
Cache-Control: max-stale[=<seconds>]
Cache-Control: min-fresh=<seconds>
Cache-Control: no-cache 
Cache-Control: no-store
Cache-Control: no-transform
Cache-Control: only-if-cached


Response Directive:
Cache-Control: must-revalidate
Cache-Control: no-cache
Cache-Control: no-store
Cache-Control: no-transform
Cache-Control: public
Cache-Control: private
Cache-Control: proxy-revalidate
Cache-Control: max-age=<seconds>
Cache-Control: s-maxage=<seconds>
"""
