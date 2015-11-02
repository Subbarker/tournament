import json
import requests
headers = {'content-type': 'application/json'}

t1 = requests.post('http://127.0.0.1:5000/v1/tournaments/').text
print(t1)
t2 = requests.post('http://127.0.0.1:5000/v1/tournaments/').text
print(t2)

names = ['BYE', 'jeff', 'shirley', 'britta', 'abed']

players = [requests.post('http://127.0.0.1:5000/v1/players/', headers=headers, data=json.dumps({'name': n})).text for n in names]
print(players)

requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 1}))
requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 2}))
requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 3}))
requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 4}))
requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 5}))


print(requests.post('http://127.0.0.1:5000/v1/matches/').text)