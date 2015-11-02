from flask import Flask, request, url_for
from sqlalchemy.exc import InvalidRequestError
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


@app.route('/v1/tournaments/<int:tournament_id>')
@jsonify
def tournament(tournament_id):
    return data(get_tournament(tournament_id))


def get_tournament(id):
    return models.Tournament.query.filter(models.Tournament.id == id).one()


@app.route('/v1/tournaments/<int:tournament_id>/players/', methods=['GET', 'POST'])
def tournament_players(tournament_id):
    if request.method == 'GET':
        return list_view(models.Player.query.join(models.Tournament.players).filter(models.Tournament.id == tournament_id))
    if request.method == 'POST':
        t = get_tournament(tournament_id)
        p = models.Player(id=int(request.json['id']))
        t.players.append(p)
        models.db.session.commit()
        return p.href


@app.route('/v1/players/', methods=['GET', 'POST'])
def players():
    if request.method == 'GET':
        return list_view(models.Player.query)
    if request.method == 'POST':
        return create_player()


def create_player():
    p = models.Player(name=request.json['name'])
    models.db.session.add(p)
    try:
        models.db.session.commit()
    except InvalidRequestError:
        models.db.session.rollback()
        return {'error': '{} already exists'.format(p.name)}, 409
    return p.href, 201


@app.route('/v1/players/<int:player_id>')
@jsonify
def player(player_id):
    return data(get_player(player_id))


def get_player(id):
    return models.Player.query.filter(models.Player.id == id).one()


if __name__ == '__main__':
    app.run(debug=True)

