from flask import Flask
from asgiref.wsgi import WsgiToAsgi
import time

app = Flask(__name__)

# to deploy it on uvicorn(ASGI), we need conversion since flask is WSGI supported framwork
wsgi = WsgiToAsgi(app)


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



"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/github-repos/atlas/hpe/atlas-opemgr-rest-server (master)
$  pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 uvicorn


Since here we are not giving here any workers, so will run one by one
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/flask_exp/uvicorn_exp
$ uvicorn --reload --host 0.0.0.0 --port 5000 flask_on_uvicorn:wsgi
INFO:     Will watch for changes in these directories: ['C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\mypy\\app\\flask_exp\\uvicorn_exp']
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started reloader process [232308] using statreload
INFO:     Started server process [33848]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
WARNING:  StatReload detected file change in 'flask_on_uvicorn.py'. Reloading...
INFO:     Started server process [248436]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
WARNING:  StatReload detected file change in 'flask_on_uvicorn.py'. Reloading...
INFO:     Started server process [254168]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
Fetching the products for user: aafak20
Fetching the products for user: aafak20, 0/10
Fetching the products for user: aafak20, 1/10
Fetching the products for user: aafak20, 2/10
Fetching the products for user: aafak20, 3/10
Fetching the products for user: aafak20, 4/10
Fetching the products for user: aafak20, 5/10
Fetching the products for user: aafak20, 6/10
Fetching the products for user: aafak20, 7/10
Fetching the products for user: aafak20, 8/10
Fetching the products for user: aafak20, 9/10
INFO:     127.0.0.1:62008 - "GET /products/aafak20 HTTP/1.1" 200 OK


Fetching the home page for user: aafak20
Fetching the page for user: aafak20, 0/10
Fetching the page for user: aafak20, 1/10
Fetching the page for user: aafak20, 2/10
Fetching the page for user: aafak20, 3/10
Fetching the page for user: aafak20, 4/10
Fetching the page for user: aafak20, 5/10
Fetching the page for user: aafak20, 6/10
Fetching the page for user: aafak20, 7/10
Fetching the page for user: aafak20, 8/10
Fetching the page for user: aafak20, 9/10
INFO:     127.0.0.1:62009 - "GET /users/aafak20 HTTP/1.1" 200 OK
Fetching the products for user: aafak10
Fetching the products for user: aafak10, 0/10
Fetching the products for user: aafak10, 1/10
Fetching the products for user: aafak10, 2/10
Fetching the products for user: aafak10, 3/10
Fetching the products for user: aafak10, 4/10
Fetching the products for user: aafak10, 5/10
Fetching the products for user: aafak10, 6/10
Fetching the products for user: aafak10, 7/10
Fetching the products for user: aafak10, 8/10
Fetching the products for user: aafak10, 9/10
INFO:     127.0.0.1:62010 - "GET /products/aafak10 HTTP/1.1" 200 OK
Fetching the home page for user: aafak10
Fetching the page for user: aafak10, 0/10
Fetching the page for user: aafak10, 1/10
Fetching the page for user: aafak10, 2/10
Fetching the page for user: aafak10, 3/10
Fetching the page for user: aafak10, 4/10
Fetching the page for user: aafak10, 5/10
Fetching the page for user: aafak10, 6/10
Fetching the page for user: aafak10, 7/10
Fetching the page for user: aafak10, 8/10
Fetching the page for user: aafak10, 9/10
INFO:     127.0.0.1:62015 - "GET /users/aafak10 HTTP/1.1" 200 OK

"""