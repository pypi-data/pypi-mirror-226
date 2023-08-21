"""
- when the client establishes a connection with the server and requests an
   encrypted connection, the server responds with its SSL Certificate.
- The certificate acts as identification for the server, as it includes the server name and domain.
- To ensure that the information provided by the server is correct, the certificate is cryptographically signed by
    a certificate authority, or CA.
- If the client knows and trusts the CA, it can confirm that the certificate signature indeed
   comes from this entity, and with this the client can be certain that the server it connected to is legitimate.
- After the client verifies the certificate, it creates an encryption key to use for the communication
   with the server
- To make sure that this key is sent securely to the server, it encrypts it using a public key that is included with the server certificate
- The server is in possession of the private key that goes with that public key in the certificate,
   so it is the only party that is able to decrypt the package.
   From the point when the server receives the encryption key all traffic is encrypted with this key that only the client and server know.

To implement TLS encryption we need two items:
 1). A server certificate, which includes a public key and is signed by a CA, and
 2). A private key that goes with the public key included in the certificate.

Flask, and more specifically Werkzeug, support the use of on-the-fly certificates, which are useful
to quickly serve an application over HTTPS without having to mess with certificates. All you need
to do, is add ssl_context='adhoc' to your app.run() call.
To use ad hoc certificates with Flask, you need to install an additional dependency in your virtual environment:
pip install pyopenssl


The problem is that browsers do not like this type of certificate,
so they show a big and scary warning that you need to dismiss before you can access the application.
Once you allow the browser to connect, you will have an encrypted connection, just like what you get
from a server with a valid certificate, which make these ad hoc certificates convenient
for quick & dirty tests, but not for any real use.
"""




from flask import Flask, make_response
from flask_api import status
from gevent.wsgi import WSGIServer
app = Flask(__name__)

@app.route("/")
def hello():
    print 'processing...'
    return make_response('success', status.HTTP_200_OK)


# https://127.0.0.1:5000/
if __name__ == "__main__":
    app.run(ssl_context='adhoc')
    #server = WSGIServer(('127.0.0.1', 5000), app, ssl_args='adhoc')
    #server.serve_forever()
