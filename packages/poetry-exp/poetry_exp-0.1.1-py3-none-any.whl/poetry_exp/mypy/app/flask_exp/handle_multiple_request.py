"""
Lighweight micro web framework based warezug and jinja2 templating
flask==0.12.2

"""


from flask import Flask
from gevent.pywsgi import WSGIServer
import time

app = Flask(__name__)


@app.route("/users/<string:username>")
def home_page(username):
    print (f"Fetching the page for user: {username}")
    for i in range(10):
        time.sleep(1)
        print(f"Fetching the page for user: {username}, {i}/10")

    return f"Welcome {username}"


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    print('Starting the server')
    server.serve_forever()

# http://127.0.0.1:5000/home


"""

Open three tab in browser and hit diffrent url
http://localhost:5000/users/aafak2
http://localhost:5000/users/aafak3
http://localhost:5000/users/aafak4

C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/app/flask_exp/handle_multiple_request.py"
Starting the server
Fetching the page for user: aafak
Fetching the page for user: aafak, 0/10
Fetching the page for user: aafak, 1/10
Fetching the page for user: aafak, 2/10
Fetching the page for user: aafak, 3/10
Fetching the page for user: aafak, 4/10
Fetching the page for user: aafak, 5/10
Fetching the page for user: aafak, 6/10
Fetching the page for user: aafak, 7/10
Fetching the page for user: aafak, 8/10
Fetching the page for user: aafak, 9/10
127.0.0.1 - - [2022-05-05 15:10:34] "GET /users/aafak HTTP/1.1" 200 129 10.002771
Fetching the page for user: aafak1
Fetching the page for user: aafak1, 0/10
Fetching the page for user: aafak1, 1/10
Fetching the page for user: aafak1, 2/10
Fetching the page for user: aafak1, 3/10
Fetching the page for user: aafak1, 4/10
Fetching the page for user: aafak1, 5/10
Fetching the page for user: aafak1, 6/10
Fetching the page for user: aafak1, 7/10
Fetching the page for user: aafak1, 8/10
127.0.0.1 - - [2022-05-05 15:10:57] "GET /users/aafak1 HTTP/1.1" 200 130 10.005395
Fetching the page for user: aafak1, 9/10
Fetching the page for user: aafak2
Fetching the page for user: aafak2, 0/10
Fetching the page for user: aafak2, 1/10
Fetching the page for user: aafak2, 2/10
Fetching the page for user: aafak2, 3/10
Fetching the page for user: aafak2, 4/10
Fetching the page for user: aafak2, 5/10
Fetching the page for user: aafak2, 6/10
Fetching the page for user: aafak2, 7/10
Fetching the page for user: aafak2, 8/10
127.0.0.1 - - [2022-05-05 15:11:59] "GET /users/aafak2 HTTP/1.1" 200 130 10.004608
Fetching the page for user: aafak2, 9/10
Fetching the page for user: aafak3
Fetching the page for user: aafak3, 0/10
Fetching the page for user: aafak3, 1/10
Fetching the page for user: aafak3, 2/10
Fetching the page for user: aafak3, 3/10
Fetching the page for user: aafak3, 4/10
Fetching the page for user: aafak3, 5/10
Fetching the page for user: aafak3, 6/10
Fetching the page for user: aafak3, 7/10
Fetching the page for user: aafak3, 8/10
127.0.0.1 - - [2022-05-05 15:12:09] "GET /users/aafak3 HTTP/1.1" 200 130 10.004078
Fetching the page for user: aafak3, 9/10
Fetching the page for user: aafak4
Fetching the page for user: aafak4, 0/10
Fetching the page for user: aafak4, 1/10
Fetching the page for user: aafak4, 2/10
Fetching the page for user: aafak4, 3/10
Fetching the page for user: aafak4, 4/10
Fetching the page for user: aafak4, 5/10
Fetching the page for user: aafak4, 6/10
Fetching the page for user: aafak4, 7/10
Fetching the page for user: aafak4, 8/10
Fetching the page for user: aafak4, 9/10
127.0.0.1 - - [2022-05-05 15:12:19] "GET /users/aafak4 HTTP/1.1" 200 130 10.003680

"""