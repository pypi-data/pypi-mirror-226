from flask import Flask
import time

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)

"""
$ pip3 install --proxy=http://web-proxy.in.hpecorp.net:8080 gunicorn

aafak@aafak-virtual-machine:~/test_py/gunicorn_exp$ python3 flask_on_gunicorn.py
 * Serving Flask app 'flask_on_gunicorn' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.17.29.165:5004/ (Press CTRL+C to quit)
^Caafak@aafak-virtual-machine:~/test_py/gunicorn_exp$ ^C

Try browsing http://172.17.29.165:5004/users/a
This site can’t be reached

aafak@aafak-virtual-machine:~/test_py/gunicorn_exp$ sudo ufw allow 5004
[sudo] password for aafak:
Rule added
Rule added (v6)
aafak@aafak-virtual-machine:~/test_py/gunicorn_exp$ python3 flask_on_gunicorn.py
 * Serving Flask app 'flask_on_gunicorn' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.17.29.165:5004/ (Press CTRL+C to quit)
Fetching the home page for user: a
Fetching the page for user: a, 0/10
Fetching the page for user: a, 1/10

Fetching the page for user: a, 2/10
Fetching the page for user: a, 3/10
Fetching the page for user: a, 4/10
Fetching the page for user: a, 5/10
Fetching the page for user: a, 6/10
Fetching the page for user: a, 7/10
Fetching the page for user: a, 8/10
Fetching the page for user: a, 9/10
172.17.160.160 - - [16/May/2022 10:48:23] "GET /users/a HTTP/1.1" 200 -
172.17.160.160 - - [16/May/2022 10:48:25] "GET /favicon.ico HTTP/1.1" 404 -
^Caafak@aafak-virtual-machine:~/test_py/gunicorn_exp$ ^C

aafak@aafak-virtual-machine:~/test_py/gunicorn_exp$ gunicorn -w 4 --bind 0.0.0.0:8004 flask_on_gunicorn:app
[2022-05-16 10:51:01 +0530] [1097385] [INFO] Starting gunicorn 20.1.0
[2022-05-16 10:51:01 +0530] [1097385] [INFO] Listening at: http://0.0.0.0:8004 (1097385)
[2022-05-16 10:51:01 +0530] [1097385] [INFO] Using worker: sync
[2022-05-16 10:51:01 +0530] [1097387] [INFO] Booting worker with pid: 1097387
[2022-05-16 10:51:01 +0530] [1097388] [INFO] Booting worker with pid: 1097388
[2022-05-16 10:51:01 +0530] [1097389] [INFO] Booting worker with pid: 1097389
[2022-05-16 10:51:01 +0530] [1097390] [INFO] Booting worker with pid: 1097390

[2022-05-16 10:58:46 +0530] [1101343] [CRITICAL] WORKER TIMEOUT (pid:1101349)
[2022-05-16 10:58:46 +0530] [1101349] [INFO] Worker exiting (pid: 1101349)
[2022-05-16 10:58:46 +0530] [1102481] [INFO] Booting worker with pid: 1102481
Fetching the home page for user: aafak1
Fetching the page for user: aafak1, 0/10
Fetching the page for user: aafak1, 1/10
Fetching the page for user: aafak1, 2/10
Fetching the page for user: aafak1, 3/10
Fetching the page for user: aafak1, 4/10
[2022-05-16 10:59:54 +0530] [1101343] [CRITICAL] WORKER TIMEOUT (pid:1102481)
[2022-05-16 10:59:54 +0530] [1102481] [INFO] Worker exiting (pid: 1102481)
[2022-05-16 10:59:54 +0530] [1103090] [INFO] Booting worker with pid: 1103090
^C[2022-05-16 11:02:44 +0530] [1101343] [INFO] Handling signal: int
[2022-05-16 11:02:44 +0530] [1103090] [INFO] Worker exiting (pid: 1103090)
[2022-05-16 11:02:44 +0530] [1101347] [INFO] Worker exiting (pid: 1101347)
[2022-05-16 11:02:44 +0530] [1101348] [INFO] Worker exiting (pid: 1101348)
[2022-05-16 11:02:44 +0530] [1101346] [INFO] Worker exiting (pid: 1101346)
^C[2022-05-16 11:02:44 +0530] [1101343] [WARNING] Worker with pid 1101346 was terminated due to signal 2
[2022-05-16 11:02:44 +0530] [1101343] [INFO] Shutting down: Master
aafak@aafak-virtual-machine:~/test_py/gunicorn_exp$ ^C


aafak@aafak-virtual-machine:~$ curl -X GET localhost:8004/users/aafak1
curl: (52) Empty reply from server
aafak@aafak-virtual-machine:~$ curl -X GET localhost:8004/users/aafak1
curl: (52) Empty reply from server


now use timout to aboid restarting of workers


aafak@aafak-virtual-machine:~/test_py/gunicorn_exp$ gunicorn -w 4 --bind 0.0.0.0:8004 --timeout 120 flask_on_gunicorn:app
[2022-05-16 11:04:59 +0530] [1105832] [INFO] Starting gunicorn 20.1.0
[2022-05-16 11:04:59 +0530] [1105832] [INFO] Listening at: http://0.0.0.0:8004 (1105832)
[2022-05-16 11:04:59 +0530] [1105832] [INFO] Using worker: sync
[2022-05-16 11:04:59 +0530] [1105834] [INFO] Booting worker with pid: 1105834
[2022-05-16 11:04:59 +0530] [1105835] [INFO] Booting worker with pid: 1105835
[2022-05-16 11:04:59 +0530] [1105836] [INFO] Booting worker with pid: 1105836
[2022-05-16 11:04:59 +0530] [1105837] [INFO] Booting worker with pid: 1105837
Fetching the home page for user: aafak1
Fetching the page for user: aafak1, 0/10
Fetching the page for user: aafak1, 1/10
Fetching the page for user: aafak1, 2/10
Fetching the page for user: aafak1, 3/10
Fetching the page for user: aafak1, 4/10
Fetching the page for user: aafak1, 5/10
Fetching the page for user: aafak1, 6/10
Fetching the page for user: aafak1, 7/10
Fetching the page for user: aafak1, 8/10
Fetching the page for user: aafak1, 9/10


aafak@aafak-virtual-machine:~$ curl -X GET localhost:8004/users/aafak1
Welcome aafak1
aafak@aafak-virtual-machine:~$



From the 4 tabs run :
aafak@aafak-virtual-machine:~$ curl -X GET localhost:8004/users/aafak1
Welcome aafak1
aafak@aafak-virtual-machine:~$
aafak@aafak-virtual-machine:~$ curl -X GET localhost:8004/products/aafak1
Products for aafak1
aafak@aafak-virtual-machine:~$
aafak@aafak-virtual-machine:~$ curl -X GET localhost:8004/users/aafak2
Welcome aafak2
aafak@aafak-virtual-machine:~$
aafak@aafak-virtual-machine:~$ curl -X GET localhost:8004/products/aafak2
Products for aafak2
aafak@aafak-virtual-machine:~$

All running in paralell..........

Fetching the home page for user: aafak1
Fetching the products for user: aafak1
Fetching the home page for user: aafak2
Fetching the page for user: aafak1, 0/10
Fetching the products for user: aafak2
Fetching the products for user: aafak1, 0/10
Fetching the page for user: aafak2, 0/10
Fetching the page for user: aafak1, 1/10
Fetching the products for user: aafak2, 0/10
Fetching the products for user: aafak1, 1/10
Fetching the page for user: aafak2, 1/10
Fetching the page for user: aafak1, 2/10
Fetching the products for user: aafak2, 1/10
Fetching the products for user: aafak1, 2/10
Fetching the page for user: aafak2, 2/10
Fetching the page for user: aafak1, 3/10
Fetching the products for user: aafak2, 2/10
Fetching the products for user: aafak1, 3/10
Fetching the page for user: aafak2, 3/10
Fetching the page for user: aafak1, 4/10
Fetching the products for user: aafak2, 3/10
Fetching the products for user: aafak1, 4/10
Fetching the page for user: aafak2, 4/10
Fetching the page for user: aafak1, 5/10
Fetching the products for user: aafak2, 4/10
Fetching the products for user: aafak1, 5/10
Fetching the page for user: aafak2, 5/10
Fetching the page for user: aafak1, 6/10
Fetching the products for user: aafak2, 5/10
Fetching the products for user: aafak1, 6/10
Fetching the page for user: aafak2, 6/10
Fetching the page for user: aafak1, 7/10
Fetching the products for user: aafak2, 6/10
Fetching the products for user: aafak1, 7/10
Fetching the page for user: aafak2, 7/10
Fetching the page for user: aafak1, 8/10
Fetching the products for user: aafak2, 7/10
Fetching the products for user: aafak1, 8/10
Fetching the page for user: aafak2, 8/10
Fetching the page for user: aafak1, 9/10
Fetching the products for user: aafak2, 8/10
Fetching the products for user: aafak1, 9/10
Fetching the page for user: aafak2, 9/10
Fetching the products for user: aafak2, 9/10




"""