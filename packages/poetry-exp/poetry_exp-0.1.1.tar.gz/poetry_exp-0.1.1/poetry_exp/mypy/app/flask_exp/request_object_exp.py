"""
The data from a clients web page is sent to the server as a global request object.
 In order to process the request data, it should be imported from the Flask module.

Important attributes of request object are listed below:
form: It is a dictionary object containing key and value pairs of form parameters and their values.
args: parsed contents of query string which is part of URL after question mark (?).
Cookies: dictionary object holding Cookie names and values.
files: data pertaining to uploaded file.
method: current request method.

"""

from flask import Flask, request, render_template
from gevent.wsgi import WSGIServer

app = Flask(__name__)


@app.route("/signup")
def sign_up():
    return render_template('signup.html')


@app.route('/createAccount', methods=['POST'])
def create_account():
    if request.method == 'POST':
        user_details = request.form
        print 'creating user: ', user_details

        # This is a immutable dict , You cannot remove items fro this
        # user_details.pop('Signup')
        # user_details.pop('password')
        return render_template('user_details.html', user=user_details)


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()