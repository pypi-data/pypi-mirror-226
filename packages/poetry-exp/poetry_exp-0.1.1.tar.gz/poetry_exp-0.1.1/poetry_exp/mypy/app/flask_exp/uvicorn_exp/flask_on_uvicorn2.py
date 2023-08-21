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
        time.sleep(6)
        print(f"Fetching the page for user: {username}, {i}/10")

    return f"Welcome {username}"


@app.route("/products/<string:username>")
def get_products(username):
    print (f"Fetching the products for user: {username}")
    for i in range(10):
        time.sleep(6)
        print(f"Fetching the products for user: {username}, {i}/10")

    return f"Products for {username}"



"""
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/github-repos/atlas/hpe/atlas-opemgr-rest-server (master)
$  pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 uvicorn
aafakmoh@WHDCIS4TDR MINGW64 ~/OneDrive - Hewlett Packard Enterprise/mypy/app/flask_exp/uvicorn_exp
$ uvicorn --workers 4 --host 0.0.0.0 --port 5000 flask_on_uvicorn2:wsgi
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Started parent process [179960]
INFO:     Started server process [152880]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Started server process [238284]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Started server process [110588]
INFO:     Application startup complete.
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Started server process [34576]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.


"""