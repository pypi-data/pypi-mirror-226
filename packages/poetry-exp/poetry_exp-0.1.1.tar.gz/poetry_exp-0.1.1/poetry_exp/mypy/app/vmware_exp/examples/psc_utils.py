import requests

username = 'root'
password = 'Password1!'
auth = requests.auth.HTTPBasicAuth(username, password)
url = 'https://psc01.pod2.local:5480/vami/backend/administration-page.py'
headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
data = "<request><locale>en-US</locale><action>query</action><requestid>authenticate</requestid></request>"
response = requests.request('POST', url, cookies=None, headers=headers, auth=auth, data=data, verify=False)
print '.......response', response
print '.......', response.content
print '.......cookies', response.cookies.get_dict()
print '....header', response.headers


#/usr/lib/vmware-vmca/bin/certificate-manager