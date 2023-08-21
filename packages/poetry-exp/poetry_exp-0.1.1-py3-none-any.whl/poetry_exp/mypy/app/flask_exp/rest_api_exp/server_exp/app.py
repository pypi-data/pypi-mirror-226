from flask import Flask, request, make_response, jsonify
from uuid import uuid4
from datetime import datetime
from gevent.wsgi import WSGIServer
from flask_api import status
from functools import wraps

app = Flask(__name__)
app.debug = True
__TOKEN = {}

# http://localhost:5000/api/v1/login/
@app.route('/api/v1/login/', methods=['POST'])
def login():
    print dir(request)
    print 'content_type: ', request.content_type
    print 'data:', request.data
    print 'get_data', request.get_data()
    json_data = request.get_json()
    username = json_data['username']
    password = json_data['password']

    token = str(uuid4())
    __TOKEN[token] = {
        'created': datetime.now(),
        'username': username
    }
    return make_response(jsonify({"Authentication-Token": token}), status.HTTP_200_OK)


def is_valid_token():
    """
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
    Connection: keep-alive
    Authentication-Token: ca1770f4-4baa-4332-93c1-bd8d7828abb6
    Postman-Token: cf579f79-2e1c-93c7-ec4f-9f9198e3e286
    Host: localhost:5000
    Cache-Control: no-cache
    Accept: application/json
    Accept-Language: en-US,en;q=0.9
    Content-Type: application/json
    Accept-Encoding: gzip, deflate, br
    """
    print request.headers
    token = request.headers['Authentication-Token']
    print 'Token: ', token
    if token in __TOKEN:
        return True
    else:
        return False


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_valid_token():
            return func(*args, **kwargs)
        else:
            error = {
                "errors": [
                    {
                        "message": "Unauthorized",
                        "error": "Invalid/Expired Token",
                        "code": 401
                    }
                ]
            }
            return make_response(jsonify(error), status.HTTP_401_UNAUTHORIZED)
    return wrapper


@app.route('/api/v1/orders/', methods=['GET'])
@token_required
def orders():
    print '................', request.query_string  #  pagelimit=20&quantity=2
    # qs_ar = request.query_string.split('&')
    # print qs_ar[0].split('=')[1]
    # print qs_ar[1].split('=')[1]
    print 'query_params: ', request.args  # ImmutableMultiDict([('color', u'red'), ('color', u'blue'), ('color', u'green'), ('pagelimit', u'20'), ('quantity', u'2')])
    print 'quantity: ', request.args.get('quantity')  # 2
    print 'color: ',request.args.get('color')
    data = request.args.to_dict(flat=False)  # {'color': [u'red', u'blue', u'green'], 'pagelimit': [u'20'], 'quantity': [u'2']}
    # data = request.args.to_dict() # {'color': u'red', 'pagelimit': u'20', 'quantity': u'2'}
    print data
    # to_dict() method to convert them to a regular dictionary.
    #print 'json: ', request.get_json()

    user_orders = [
        {
            "id": 1,
            "name": 'TV'
        },
        {
            "id": 2,
            "name": 'Referizator'
        }
    ]

    return make_response(jsonify(user_orders), status.HTTP_200_OK)


@app.route('/api/v1/orders/', methods=['POST'])
@token_required
def place_order():
    order_data = request.get_json()
    p_name = order_data['name']
    p_amount = order_data['amount']
    print 'placing order'
    return make_response(jsonify({"name": p_name, "amount": p_amount}), status.HTTP_201_CREATED)


@app.route('/api/v1/orders/<orderId>', methods=['PUT'])
@token_required
def update_order(orderId):
    order_data = request.get_json()
    qty = order_data['quantity']
    print 'Updating order...', orderId

    return make_response(jsonify({"success": True}), status.HTTP_200_OK)



@app.route('/api/v1/orders/<orderId>', methods=['DELETE'])
@token_required
def delete_order(orderId):
    print 'Deleting order...', orderId
    return make_response(jsonify({"success": True}), status.HTTP_204_NO_CONTENT)



# https://www.snyxius.com/21-best-practices-designing-launching-restful-api/
# sub-resources relationship

@app.route('/api/v1/users/<userId>/orders/')
@token_required
def user_orders(userId):
    print "User's orderes"
    user_orders = [
        {
            "id": 1,
            "name": 'TV'
        },
        {
            "id": 2,
            "name": 'Referizator'
        }
    ]

    return make_response(jsonify(user_orders), status.HTTP_200_OK)


if __name__ == '__main__':
    server = WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()