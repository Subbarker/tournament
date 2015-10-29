from flask import Flask, request, url_for
import models
from tools import jsonify, data

app = Flask(__name__)


@app.before_first_request
def setup():
    models.db.create_all()


@app.route('/v1/')
@jsonify
def root():
    return {
        'tournaments': url_for('tournaments', _external=True)
    }


@app.route('/v1/tournaments/', methods=['GET', 'POST'])
def tournaments():
    if request.method == 'GET':
        return list_view(models.Tournament.query)
    if request.method == 'POST':
        return create_tournament()


@jsonify
def list_view(q):
    return {'content': [o.href for o in q]}


def create_tournament():
    t = models.Tournament()
    models.db.session.add(t)
    models.db.session.commit()
    return t.href, 201


@app.route('/v1/tournaments/<int:tournament_id>', methods=['GET'])
@jsonify
def tournament(tournament_id):
    if request.method == 'GET':
        return data(get_tournament(tournament_id))


def get_tournament(id):
    return models.Tournament.query.filter(models.Tournament.id == id).one()


@app.route('/v1/tournaments/<int:tournament_id>/players/', methods=['GET', 'POST'])
def tournament_players(tournament_id):
    if request.method == 'GET':
        return list_view(models.Player.query.join(models.Tournament.players).filter(models.Tournament.id == tournament_id))
    if request.method == 'POST':
        t = get_tournament(tournament_id)
        p = models.Player(id=int(request.json()['id']))
        t.players.append(models.db.session.merge(p))


if __name__ == '__main__':
    app.run(debug=True)

