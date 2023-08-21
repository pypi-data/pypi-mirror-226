"""
Lighweight micro web framework based warezug and jinja2 templating
flask==0.12.2

"""


from flask import Flask
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route("/home")
def home_page():
    print ("Fetching the page....")
    return "Welcome to Flask"


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    print('Starting the server')
    server.serve_forever()

# http://127.0.0.1:5000/home