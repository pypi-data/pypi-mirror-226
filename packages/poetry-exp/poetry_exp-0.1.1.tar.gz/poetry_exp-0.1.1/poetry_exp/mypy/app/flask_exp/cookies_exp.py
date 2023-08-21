"""
A cookie is stored on a clients computer in the form of a text file.
Its purpose is to remember and track data pertaining to a clients usage
 for better visitor experience and site statistics.

 A Request object contains a cookies attribute. It is a dictionary object of all the
 cookie variables and their corresponding values, a client has transmitted.
 In addition to it, a cookie also stores its expiry time, path and domain name of the site.

In Flask, cookies are set on response object. Use make_response() function to
get response object from return value of a view function.
After that, use the set_cookie() function of response object to store a cookie.

The get() method of request.cookies attribute is used to read a cookie.
"""

from flask import Flask, make_response, render_template, request
from gevent.wsgi import WSGIServer

app = Flask(__name__)


"""
For rest api:
    if not response:
        input_error = {
            "ErrorMessage": "Authentication Failed"
        }
        return make_response(jsonify(input_error),
                      status.HTTP_400_BAD_REQUEST)
    report['response'] = response
    return make_response(jsonify(report),
                         status.HTTP_200_OK)
"""

@app.route('/')
def home():
    return render_template('cookie_exp.html')


@app.route('/setCookies', methods=['POST'])
def set_cookies():
    if request.method == 'POST':
        user = request.form['name']

    resp = make_response(render_template('read_cookies.html'))
    resp.set_cookie('userId', user)
    return resp


@app.route('/getCookies')
def get_cookies():
    name = request.cookies.get('userId')
    return "<h1> Welcome " + name + "</h1>"


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()