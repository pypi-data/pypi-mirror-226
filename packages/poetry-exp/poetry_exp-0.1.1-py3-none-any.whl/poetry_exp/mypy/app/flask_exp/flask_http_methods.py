"""
Http protocol is the foundation of data communication in world wide web.
Different methods of data retrieval from specified URL are defined in this protocol.

By default, the Flask route responds to the GET requests. However, this preference can be altered by
providing methods argument to route()decorator.

GET: Sends data in unencrypted form to the server. Most common method.
HEAD: Same as GET, but without response body
POST: Used to send HTML form data to server. Data received by POST method is not cached by server.
PUT: Replaces all current representations of the target resource with the uploaded content.
DELETE: Removes all current representations of the target resource given by a URL

Flask is based on jinja2 template
The term web templating system refers to designing an HTML script in which the variable data can be
 inserted dynamically. A web template system comprises of a template engine,
  some kind of data source and a template processor
"""

from flask import Flask, render_template, request, redirect, url_for
from gevent.wsgi import WSGIServer

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('login.html')
    # Flask will try to find the HTML file in the templates folder, in the same folder in which this script is present


@app.route('/success/<username>')
def success(username):
    return "Welcome: {0}".format(username)


# @app.route("/login", methods=['POST', 'GET]) is also valid same request will work for both
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('success', username=username))  # will redirect to http://localhost:5000/success/admin
    else:
        """args is dictionary object containing a list of pairs of form parameter and its corresponding value."""
        username = request.args.get('username')
        return redirect(url_for('success', username=username))


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()

