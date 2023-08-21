import requests
import json

def get_token():
    url = "https://172.17.29.164/rest/rm-central/v1/login-sessions"
    body = {
        "auth": {
            "passwordCredentials": {
                "username": "Admin",
                "password": "12rmc*Help"
            }
        }
    }
    headers={
        "Content-Type": "application/json"
    }
    print json.dumps(body)
    response = requests.post(url, data=json.dumps(body), auth=("Admin", "12rmc*Help"), headers=headers, verify=False)
    print response.json()
    token =  response.json()['loginSession']['access']['token']['id']
    print token
    return token


token =  get_token()
headers = {
    'X-Auth-Token': token,
    'Accept': 'application/json'
}
#url = "https://172.17.29.166/rest/rm-central/v1/storage-systems"
#response = requests.get(url=url, headers=headers, verify=False)

url = "https://172.17.29.164:8000/rest/rmcv/v1/storage-device-collections"
body = {
  "filePath": "/root/rc_group.json"
}
response = requests.put(url=url, data=json.dumps(body), headers=headers, verify=False)
print response.json()