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

"""
https://felipefaria.medium.com/running-a-simple-flask-application-inside-a-docker-container-b83bf3e07dd5
Notice that inside the app.run() params we have host="0.0.0.0". This is a necessity as 0.0.0.0 is
a wildcard IP address that will match any possible incoming port on the host machine.
We require this because port 127.0.0.1 inside a Docker container does not actually get captured and
exposed into the host machine.
Flask automatically sets the application port to 5000 but we changed that by setting
the variable port inside to port 5001.
"""