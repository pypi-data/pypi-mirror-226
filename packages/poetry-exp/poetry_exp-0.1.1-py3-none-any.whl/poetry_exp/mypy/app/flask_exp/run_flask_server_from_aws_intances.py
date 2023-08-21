# Create an intance on AWS(ubuntu)
# Genrate and save the key pai
# Once started, will give you one public IP: 52.15.159.80
# from key pair generate .pkk file using putty gkey genrator
# and login through putty using useranme@public(ubuntu@52.15.159.80)
# IP, and in SSH->Auth->browse that key
# similar in WIn scp, click on advanced settings ->SSH-> Authentications=>Private key file(.ppk)
#ubuntu@ip-172-31-35-164:~/aafak$ sudo apt install python3-pip
#ubuntu@ip-172-31-35-164:~/aafak$ pip3 install flask
# ubuntu@ip-172-31-35-164:~/aafak$ pip3 install gevent
# and create one sample flask APP
# Modify the inbound rules of AWS instance
"""
Inbound rules:
80	TCP	0.0.0.0/0	launch-wizard-14
All	All	0.0.0.0/0	launch-wizard-14
22	TCP	0.0.0.0/0	launch-wizard-14
443	TCP	0.0.0.0/0	launch-wizard-14

Outbound rules:
All	All	0.0.0.0/0	launch-wizard-14


"""

from flask import Flask
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route("/home")
def home_page():
    print ("Fetching the page....")
    return "Welcome to Flask"


if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 5000), app)
    print('Starting the server')
    server.serve_forever()


# run python3 server.py
# Now browsed ti from anywhere
# http://52.15.159.80:5000/home