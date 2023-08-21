from flask import Flask
app = Flask(__name__)


@app.route("/")
def handle_alert():
    print("Handling alert....")
    return "Ok"


if __name__ == '__main__':
    print('Starting the server')
    server = app.run('172.17.29.165', 5001)
