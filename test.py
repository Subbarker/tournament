# import json
# import requests
# headers = {'content-type': 'application/json'}
#
# t1 = requests.post('http://127.0.0.1:5000/v1/tournaments/').text
# print(t1)
# t2 = requests.post('http://127.0.0.1:5000/v1/tournaments/').text
# print(t2)
#
# names = ['BYE', 'jeff', 'shirley', 'britta', 'abed']
#
# players = [requests.post('http://127.0.0.1:5000/v1/players/', headers=headers, data=json.dumps({'name': n})).text for n in names]
# print(players)
#
# requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 1}))
# requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 2}))
# requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 3}))
# requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 4}))
# requests.post(t1 + '/players/', headers=headers, data=json.dumps({'id': 5}))
#
#
# print(requests.post('http://127.0.0.1:5000/v1/matches/', headers=headers, data=json.dumps({'tournament_id': 1, 'player_1_id': 2, 'player_2_id': 3})).text)
# print(requests.post('http://127.0.0.1:5000/v1/matches/').text)
#
# requests.put('http://127.0.0.1:5000/v1/matches/2', headers=headers, data=json.dumps({'player_1_id': 4}))
import json
from models import app
import os
import tempfile
import unittest


class TournamentTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_directory(self):
        rv = self.app.get('/v1/')
        data = json.loads(rv.data.decode())

        assert 'matches' in data
        assert 'players' in data
        assert 'tournaments' in data

        assert self.app.get(data['matches']).default_status == 200
        assert self.app.get(data['players']).default_status == 200
        assert self.app.get(data['tournaments']).default_status == 200

    def create_player(self, name):
        return self.app.post('/v1/players/', data={'name': name})

    def test_players(self):
        jeff = self.create_player('jeff')
        print(4)

        assert jeff.default_status == 201
        assert self.app.get(jeff.text).default_status == 200

    def test_tournament(self):
        tournament = self.app.post('/v1/tournaments/')

        assert tournament.default_status == 201
        assert self.app.get(tournament.text).default_status == 200

if __name__ == '__main__':
    unittest.main()
