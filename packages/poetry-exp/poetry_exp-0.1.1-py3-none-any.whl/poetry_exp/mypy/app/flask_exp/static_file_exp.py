"""
A web application often requires a static file such as a javascript file or a CSSfile
supporting the display of a web page. Usually, the web server is configured to serve them for you,
 but during the development, these files are served from static folder in your package or next
  to your module and it will be available at /static on the application.
A special endpoint static is used to generate URL for static files.
In the following example, a javascript function defined in hello.js is called on OnClick event
 of HTML button in index.html, which is rendered on / URL of the Flask application
"""

from flask import Flask, render_template
from gevent.wsgi import WSGIServer

app = Flask(__name__)


@app.route("/hello")
def hello():
    return render_template('hello2.html')


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()