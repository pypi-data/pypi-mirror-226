import requests, json

"""
Accept indicates what kind of response from the server the client can accept.
Content-type always is about the content of the current request or response.
So if your request has no payload, you don't use a content-type request header.


Accept header is used by HTTP clients to tell the server which type of content they expect/prefer as response.
Content-type can be used both by clients and servers to identify the format
of the data in their request (client) or response (server)
"""


def login():
    headers = {
        "Content-Type": "application/json",  # If you don't add this, request module will not send data in json format
        "accept": "text/html" # If you don't add , it is ok, because client kno
    }
    data = {
        "username": "admin",
        "password": "Password123!"
    }
    url = "http://localhost:5000/api/v1/login/"
    # resp = requests.post(url=url, data=data, headers=headers) # will raise 400, because data is not provided in json format
    resp = requests.post(url=url, data=json.dumps(data), headers=headers)
    """
    [ 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers',
     'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines',
      'json', 'links', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']

    """
    print resp.text
    if resp.status_code == 200:
        print type(resp.text)  # unicode
        print type(resp.json)
        resp_data = resp.json()
        token = resp_data['Authentication-Token']
        print token
        return token


def get_orders(token):
   print 'Token:', token
   headers = {
       "Content-Type": "application/json",  # If you don't add this, request module will not send data in json format
       "accept": "application/json",  # If you don't add , it is ok, because client kno
       "Authentication-Token": token
   }
   #url = "http://localhost/api/v1/orders/"  # HTTPConnectionPool(host='localhost', port=80): Max retries exceeded with url: /api/v1/orders/
   url = "http://localhost:5000/api/v1/orders/"
   #resp = requests.get(url=url, headers=headers)
   resp = requests.get(url=url, headers=headers, params={'color': ['red','blue','green'],'quantity': 2, 'pagelimit':20})
   #will form the url http://localhost:5000/api/v1/orders/?color=red&color=blue&color=green&pagelimit=20&quantity=2
   print resp.text
   print resp.url
   if resp.status_code == 200:
       print resp.json()


def place_order(token):
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authentication-Token": token
    }
    data = {
        "name": 'TV',
        "amount": 50000
    }
    url = 'http://localhost:5000/api/v1/orders/'
    resp = requests.post(url=url, data=json.dumps(data), headers=headers)
    print resp
    if resp.status_code == 201:
        print resp.json()
        print 'created'


def update_order(token):
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authentication-Token": token
    }
    data = {
        "name": 'TV',
        "amount": 50000,
        "quantity": 2
    }
    url = 'http://localhost:5000/api/v1/orders/1'
    resp = requests.put(url=url, data=json.dumps(data), headers=headers)
    print resp
    if resp.status_code == 200:
        print resp.json()
        print 'updated'


def delete_order(token):
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authentication-Token": token
    }

    url = 'http://localhost:5000/api/v1/orders/1'
    resp = requests.delete(url=url, headers=headers)
    print resp
    if resp.status_code == 204:
        print 'Deleted'



def get_user_orders(token):
   print 'Token:', token
   headers = {
       "Content-Type": "application/json",  # If you don't add this, request module will not send data in json format
       "accept": "application/json",  # If you don't add , it is ok, because client kno
       "Authentication-Token": token
   }
   url = "http://localhost:5000/api/v1/users/1/orders/"
   resp = requests.get(url=url, headers=headers)
   print resp.text
   print resp.url
   if resp.status_code == 200:
       print resp.json()


if __name__ == '__main__':
    token = login()
    # place_order(token)
    get_orders(token)
    # update_order(token)
    # delete_order(token)
    # get_user_orders(token)