import requests
import base64
import six

client_id = '84f79134cc6341df9ee8c8a43cca3ec7'
client_secret = 'b48317acf809490db2e8b021b85ade71'

auth_header = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii'),
'scopes': 'user-read-recently-played'
}


data = {
  # 'grant_type': 'client_credentials'
  'grant_type': 'authorization_code'
}

response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
print(response.json())
token = response.json()['access_token']
print(token)

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
}

response = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers)

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token,
}

response = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers)


print(response.json())
print(response)
