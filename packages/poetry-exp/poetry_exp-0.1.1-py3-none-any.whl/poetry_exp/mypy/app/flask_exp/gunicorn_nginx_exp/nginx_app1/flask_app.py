from flask import Flask
app = Flask(__name__)

@app.route("/app1/api/v1/")
def index():
    return "<h1 style='color:blue'>Welcome to Index!</h1>"

@app.route("/app1/api/v1/home")
def home():
    return "<h1 style='color:blue'>Welcome to Home!</h1>"

@app.route("/app1/api/v1/users")
def users():
    return "<h1 style='color:blue'>Welcome to Users!</h1>"



if __name__ == "__main__":
    app.run(host='0.0.0.0')
