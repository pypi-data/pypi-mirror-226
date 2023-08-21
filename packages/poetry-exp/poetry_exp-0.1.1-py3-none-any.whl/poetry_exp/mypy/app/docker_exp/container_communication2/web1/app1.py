from flask import Flask
import requests
from gevent.pywsgi import WSGIServer

import os
app = Flask(__name__)


@app.route('/get_message')
def get_message():
    # To disable proxy
    session = requests.Session()
    session.trust_env = False
    #os.environ['NO_PROXY'] = 'web2:5003'

    #response = session.get('http://www.stackoverflow.com')
    message = session.get('http://web2:5003/return_message')
    #message = requests.get('http://web2:5003/return_message')

    print(f"Response from web2: {message}, text: {message.text}")
    return message.text

   """
   If you use localhost inside the container, you try to reach the container itself not possible
    to access another container. Use the service name(web2) instead or host IP to reach the
    container from a web brower. You should remove the link, it used to alias the service name.
   """


if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    server = WSGIServer(('0.0.0.0', 5002), app)
    print('Starting the server1 on port 5002')
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