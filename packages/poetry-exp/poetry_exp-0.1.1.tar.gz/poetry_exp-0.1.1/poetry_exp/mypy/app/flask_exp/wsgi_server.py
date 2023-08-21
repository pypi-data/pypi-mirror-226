"""

What is a WSGI server?
WSGI is a specification, for a standardized interface between Web servers and Python Web frameworks/applications.
The goal is to provide a relatively simple yet comprehensive interface capable of supporting all (or most)
interactions between a Web server and a Web framework.

Flasks built-in server is not suitable for production as it does not scale well
and by default serves only one request at a time.
Some of the options available for properly running Flask in production are documented here.

If you want to deploy your Flask application to a WSGI server not listed here,
look up the server documentation about how to use a WSGI app with it.
 Just remember that your Flask application object is the actual WSGI application.

Gevent is a coroutine-based Python networking library that uses greenlet to provide
a high-level synchronous API on top of libev event loop:

greenlet:Lightweight concurrent programming
greenlet is a micro-thread with no implicit scheduling; coroutines,
in other words. This is useful when you want to control exactly when your code runs.
You can build custom scheduled micro-threads on top of greenlet; however, it seems that greenlets
are useful on their own as a way to make advanced control flow structures.
 For example, we can recreate generators; the difference with Pythons own generators is that our
  generators can call nested functions and the nested functions can yield values too. (Additionally, you dont need a yield
   keyword


from greenlet import greenlet

def test1():
    print(12)
    gr2.switch()
    print(34)

def test2():
    print(56)
    gr1.switch()
    print(78)

gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()

The last line jumps to test1, which prints 12, jumps to test2, prints 56, jumps back into test1,
 prints 34; and then test1 finishes and gr1 dies. At this point, the execution comes back to the original gr1.switch() call.
  Note that 78 is never printed.
"""

from gevent.wsgi import WSGIServer
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


http_server = WSGIServer(('localhost', 5002), app)
http_server.serve_forever()

# Open the browser and type the URL: http://localhost:5002/
