from flask import Flask
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/return_message')
def return_message():
    print("Returning the message.......")
    return 'the message'


if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    server = WSGIServer(('0.0.0.0', 5003), app)
    print('Starting the server1 on port 5003')
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