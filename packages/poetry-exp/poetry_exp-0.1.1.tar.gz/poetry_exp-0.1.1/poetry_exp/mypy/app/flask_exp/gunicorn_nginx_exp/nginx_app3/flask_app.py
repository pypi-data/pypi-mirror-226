from flask import Flask
app = Flask(__name__)

@app.route("/api/v1/")
def index():
    return "<h1 style='color:blue'>[app3]Welcome to Index!</h1>"

@app.route("/api/v1/home")
def home():
    return "<h1 style='color:blue'>[app3]Welcome to Home!</h1>"

@app.route("/api/v1/users")
def users():
    return "<h1 style='color:blue'>[app3]Welcome to Users!</h1>"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
