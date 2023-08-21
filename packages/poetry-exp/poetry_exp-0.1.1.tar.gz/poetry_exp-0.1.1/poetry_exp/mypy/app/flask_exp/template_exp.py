"""
Flask uses jinja2 template engine. A web template contains HTML syntax interspersed placeholders
 for variables and expressions (in these case Python expressions) which are replaced values when the template is render

 The jinja2 template engine uses the following delimiters for escaping from HTML.
{% ... %} for Statements
{{ ... }} for Expressions to print to the template output
{# ... #} for Comments not included in the template output
# ... ## for Line Statements
"""

from flask import Flask, render_template
from gevent.wsgi import WSGIServer


app = Flask(__name__)


@app.route("/user/<user>")
def hello_user(user):
    user_details = {
        "id": 1,
        "DOB": '17/03/1989',
        'Gender': 'M'
    }
    return render_template('hello.html', name=user, details=user_details)


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()

# http://127.0.0.1:5000/user/john