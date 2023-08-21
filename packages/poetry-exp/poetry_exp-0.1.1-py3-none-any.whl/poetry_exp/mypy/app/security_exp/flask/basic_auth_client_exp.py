import requests
import base64


def login():
    url = "http://localhost:5000/api/v1/login"
    print base64.b64encode(b'admin:Password123!')
    headers = {
        "Content-Type": "application/json",  # If you don't add this, request module will not send data in json format
        "accept": "application/json",  # If you don't add , it is ok, because client kno
        "Authorization": "Basic " + base64.b64encode(b'admin:Password123!')
    }

    resp = requests.post(url=url, headers=headers)
    print resp

    if resp.status_code == 200:
        print 'login success'
    else:
        print 'login failed'


def login2():
    url = "http://localhost:5000/api/v1/login"
    print base64.b64encode(b'admin:Password123!')
    headers = {
        "Content-Type": "application/json",  # If you don't add this, request module will not send data in json format
        "accept": "application/json",  # If you don't add , it is ok, because client kno
    }

    resp = requests.post(url=url, headers=headers, auth=('admin', 'Password123!'))
    print resp

    if resp.status_code == 200:
        print 'login success'
    else:
        print 'login failed'


if __name__ == '__main__':
    login()
    login2()