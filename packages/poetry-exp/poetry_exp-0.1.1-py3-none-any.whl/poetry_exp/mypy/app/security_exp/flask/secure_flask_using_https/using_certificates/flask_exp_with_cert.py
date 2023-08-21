

from flask import Flask, make_response
from flask_api import status
from gevent.wsgi import WSGIServer
app = Flask(__name__)

@app.route("/")
def hello():
    print 'processing...'
    return make_response('success', status.HTTP_200_OK)


# https://127.0.0.1:5000/ Just start this from browser and check the cert details
if __name__ == "__main__":
    server = WSGIServer(('127.0.0.1', 5000), app, keyfile='key.pem', certfile='cert.pem')
    server.serve_forever()

    #app.run(ssl_context=('cert.pem', 'key.pem'))