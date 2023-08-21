"""
Lighweight micro web framework based warezug and jinja2 templating
flask==0.12.2

"""


from flask import Flask
from gevent.pywsgi import WSGIServer
from gevent import monkey, sleep
monkey.patch_all()  # # need to patch sockets to make requests async

import time

app = Flask(__name__)


@app.route("/users/<string:username>")
def home_page(username):
    print (f"Fetching the home page for user: {username}")
    for i in range(10):
        time.sleep(1)
        print(f"Fetching the page for user: {username}, {i}/10")

    return f"Welcome {username}"


@app.route("/products/<string:username>")
def get_products(username):
    print (f"Fetching the products for user: {username}")
    for i in range(10):
        time.sleep(1)
        print(f"Fetching the products for user: {username}, {i}/10")

    return f"Products for {username}"

if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    print('Starting the server')
    server.serve_forever()
    #app.run(threaded=True)
# https://medium.com/@side_swail/how-does-python-handle-multiple-web-requests-29787925775
# http://127.0.0.1:5000/home


"""

Open three tab in browser and hit diffrent url
http://localhost:5000/users/aafak10
http://localhost:5000/products/aafak10
http://localhost:5000/users/aafak20


C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/app/flask_exp/handle_multiple_request3.py"
Starting the server
Fetching the home page for user: aafak10
Fetching the page for user: aafak10, 0/10
Fetching the page for user: aafak10, 1/10
Fetching the page for user: aafak10, 2/10
Fetching the products for user: aafak10
Fetching the page for user: aafak10, 3/10
Fetching the products for user: aafak10, 0/10
Fetching the page for user: aafak10, 4/10
Fetching the products for user: aafak10, 1/10
Fetching the page for user: aafak10, 5/10
Fetching the products for user: aafak10, 2/10
Fetching the products for user: aafak20
Fetching the page for user: aafak10, 6/10
Fetching the products for user: aafak10, 3/10
Fetching the products for user: aafak20, 0/10
Fetching the page for user: aafak10, 7/10
Fetching the products for user: aafak10, 4/10
Fetching the products for user: aafak20, 1/10
Fetching the page for user: aafak10, 8/10
Fetching the products for user: aafak10, 5/10
Fetching the products for user: aafak20, 2/10
127.0.0.1 - - [2022-05-05 16:05:31] "GET /users/aafak10 HTTP/1.1" 200 131 10.006221
Fetching the page for user: aafak10, 9/10
Fetching the products for user: aafak10, 6/10
Fetching the products for user: aafak20, 3/10
Fetching the products for user: aafak10, 7/10
Fetching the products for user: aafak20, 4/10
Fetching the products for user: aafak10, 8/10
Fetching the products for user: aafak20, 5/10
127.0.0.1 - - [2022-05-05 16:05:34] "GET /products/aafak10 HTTP/1.1" 200 136 10.005924
Fetching the products for user: aafak10, 9/10
Fetching the products for user: aafak20, 6/10
Fetching the products for user: aafak20, 7/10
Fetching the products for user: aafak20, 8/10
Fetching the products for user: aafak20, 9/10
127.0.0.1 - - [2022-05-05 16:05:38] "GET /products/aafak20 HTTP/1.1" 200 136 10.004924




"""