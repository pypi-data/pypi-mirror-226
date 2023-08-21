"""

url_for() function is very useful for dynamically building a URL for a specific function.
 The function accepts the name of a function as first argument, and one or more keyword arguments,
  each corresponding to the variable part of URL.
"""


from flask import Flask, redirect, url_for
from gevent.wsgi import WSGIServer

app = Flask(__name__)


@app.route("/admin")
def hello_admin():
    return "Hello Admin"


@app.route("/guest/<guest>")
def hello_guest(guest):
    return "Hello Guest: {0}".format(guest)


@app.route("/user/<name>")
def hello_user(name):

    if name == 'admin':
        return redirect(url_for("hello_admin"))
    else:
        return redirect(url_for("hello_guest", guest=name))

# http://127.0.0.1:5000/user/john  will be redirected to http://127.0.0.1:5000/guest/john
# http://127.0.0.1:5000/user/admin will be redirected to http://127.0.0.1:5000/admin

if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()