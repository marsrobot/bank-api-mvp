import requests
import pprint

NEWBANK_SERVER = 'MYSERVERIP'
NEWBANK_API_PORT = 8080

username = '***'
password = '***'

contents = requests.post(url=f'http://{NEWBANK_SERVER}:{NEWBANK_API_PORT}/login',
                         json={'username': username, 'password': password})

access_token = contents.json()['access_token']

contents = requests.get(url=f'http://{NEWBANK_SERVER}:{NEWBANK_API_PORT}/transactions',
                        headers={'Authorization': 'Bearer ' + access_token})

assert (contents.status_code == 200)
data = contents.json()['data']

print('Debit Transaction List:')
for i in range(len(data)):
    print('=' * 80)
    print(f'Transaction: {i + 1}')
    print('=' * 80)
    item = data[i]
    pprint.pprint(item)
