"""
Lighweight micro web framework based warezug and jinja2 templating
flask==0.12.2

"""


from flask import Flask
from gevent.pywsgi import WSGIServer
import time
app = Flask(__name__)


@app.route("/home")
def home_page():
    print ("Fetching the page....")
    time.sleep(1)
    return "Welcome to Home Page"


@app.route("/index")
def index_page():
    print("Fetching the Index Page...")
    time.sleep(1)
    return "Welcome to Index Page"


@app.route("/admin")
def admin_page():
    print("Fetching the admin page..")
    time.sleep(1)
    return "Welcome to Admin Page"


@app.route("/products")
def product_page():
    print("Fetching the product page..")
    time.sleep(1)
    return "Welcome to Product Page"


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    print('Starting the server')
    server.serve_forever()

# http://127.0.0.1:5000/home