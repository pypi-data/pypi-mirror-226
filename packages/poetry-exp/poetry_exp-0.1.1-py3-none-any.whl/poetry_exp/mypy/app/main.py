from flask import Flask
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route("/home")
def home_page():
    print ("Fetching the page....")
    return "Welcome to Flask App"


if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 5001), app)
    print('Starting the server')
    server.serve_forever()