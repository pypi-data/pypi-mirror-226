"""
Unlike a Cookie, Session data is stored on server.
Session is the time interval when a client logs into a server and logs out of it.
The data, which is needed to be held across this session, is stored in a temporary directory on the server.
A session with each client is assigned a Session ID. The Session data is stored on top of
cookies and the server signs them cryptographically.
For this encryption, a Flask application needs a defined SECRET_KEY.
Session object is also a dictionary object containing key-value pairs of session variables and associated values.

"""
from flask import Flask, session, render_template, request, url_for, redirect
from gevent.wsgi import WSGIServer

app = Flask(__name__)

# It is needed to use the session, otherwise it will throws the error
# The session is unavailable because no secret key was set.
# Set the secret_key on the application to something unique and secret.
app.secret_key = 'Secret key'


@app.route('/login')
def login():
    return render_template('login2.html')


@app.route('/')
def index():
    if 'username' in session:
        user_name = session['username']
        return "You are logged in as " + user_name + "</br>" + \
            "<b> <a href='profile'>profile</a></b>" + \
            "</br><b> <a href='logout'>Click here to logout</a></b>"
    else:
        return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))


@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verify username and password if valid add it to session
        if username == 'admin' and password == '123':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return "Invalid username or password</br>" +\
                   "<b> <a href='/'>Click here to login</a></b>"


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()