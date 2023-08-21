from flask import Flask
from gevent.wsgi import WSGIServer

app = Flask(__name__)

"""
route(rule, options)
the rule parameter of route() decorator contains <name> variable part attached to URL /post.

The URL rules of Flask are based on Werkzeugs routing module. This ensures that the URLs formed are unique
 and based on precedents laid down by Apache.
 
Adding trailing slash (/) in the URL make it cannonical, means using 
e.g 
@app.route("/flask)
@app.route("/python/")
/python or /python/ returns the same output. However, in case of the first rule, /flask/ URL results in 404 Not Found
 
"""

# http://127.0.0.1:5000/post/1
@app.route("/post/<int:postID>")
def get_post(postID):
    return "Details of Post: {0}".format(postID)


# http://127.0.0.1:5000/rev/1.5
@app.route("/rev/<float:revNum>")
def get_rev(revNum):
    return "Revision:{0}".format(revNum)


# http://127.0.0.1:5000/user/john
@app.route("/user/<username>")
def get_user(username):
    return "User:{0}".format(username)


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()