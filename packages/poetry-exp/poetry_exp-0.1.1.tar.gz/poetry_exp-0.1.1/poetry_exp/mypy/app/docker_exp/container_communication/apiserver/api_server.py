from flask import Flask
from gevent.pywsgi import WSGIServer
import requests
app = Flask(__name__)


@app.route("/home")
def home_page():
    print ("[ApiServer]: Fetching the page....")
    return "Flask Api Server ready"

@app.route("/users")
def users():
    """
    Before this DB server build and run and then do
    docker inspect network bridge
    and get the IP Address assigned for the Db server container and use that
    :return:
    """
    print ("[Server2]: Fetching the page from server1 running n another container....")
    session = requests.Session()
    session.trust_env = False
    # message = requests.get('http://172.18.0.2:5002/users')
    message = session.get('http://172.18.0.2:5002/users')

    print (f"[Server2]: Response from server1: {message}, {message.text}")
    return message.text

if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 5003), app)
    print('Starting the Api Server on port 5003')
    server.serve_forever()

"""
https://felipefaria.medium.com/running-a-simple-flask-application-inside-a-docker-container-b83bf3e07dd5
Notice that inside the app.run() params we have host="0.0.0.0". This is a necessity as 0.0.0.0 is
a wildcard IP address that will match any possible incoming port on the host machine.
We require this because port 127.0.0.1 inside a Docker container does not actually get captured and
exposed into the host machine.
Flask automatically sets the application port to 5000 but we changed that by setting
the variable port inside to port 5003.
"""