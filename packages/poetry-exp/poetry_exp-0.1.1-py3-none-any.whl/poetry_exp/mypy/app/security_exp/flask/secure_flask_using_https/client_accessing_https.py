import requests






def login():
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    url = "https://localhost:5000/"

    resp = requests.get(url=url)
    print resp

    if resp.status_code == 200:
        print 'login success'
    else:
        print 'login failed'


# requests.exceptions.SSLError: ("bad handshake: Error([('SSL routines', 'SSL23_GET_SERVER_HELLO', 'unknown protocol')],)",)
def login2():
    url = "https://localhost:5000/"

    resp = requests.get(url=url)
    print resp

    if resp.status_code == 200:
        print 'login success'
    else:
        print 'login failed'

if __name__ == '__main__':
    login()

    #login()
