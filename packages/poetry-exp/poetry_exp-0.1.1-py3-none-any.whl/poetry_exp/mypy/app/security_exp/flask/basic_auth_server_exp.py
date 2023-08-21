from flask import Flask, request, make_response, jsonify
from flask_api import status

app = Flask(__name__)

@app.route('/api/v1/login', methods=['POST'])
def login():
    auth_obj = request.authorization
    if auth_obj and auth_obj.username == 'admin' and auth_obj.password == 'Password123!':
        return make_response(jsonify({"token": "abc"}), status.HTTP_200_OK)
    else:
        return make_response(jsonify({"error": "Unauth"}), status.HTTP_401_UNAUTHORIZED)

if __name__ == '__main__':
    app.run('localhost', 5000)