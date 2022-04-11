import requests

myToken = '<token>'
myUrl = '<website>'
head = {'Authorization': 'token {}'.format(myToken)}
response = requests.get(myUrl, headers=head)

import requests

response = requests.get('https://website.com/id', headers={'Authorization': 'access_token myToken'})


import requests, json
data = { 'username' : 'root', 'password' : 'default' }
r = requests.post('https://address.of.opengear/api/v1/sessions/', data=json.dumps(data), verify=False)
token = json.loads(r.text)['session']

headers = { 'Authorization' : 'Token ' + token }
r = requests.get('https://address.of.opengear/api/v1/serialPorts/', headers=headers, verify=False)
j = json.loads(r.text)
print(json.dumps(j, indent=4))
