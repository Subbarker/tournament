from flask import Flask, request, url_for
from sqlalchemy.exc import InvalidRequestError

import models
from tools import jsonify, data, list_view, simple_filter

app = Flask(__name__)


@app.before_first_request
def setup():
    models.db.create_all()


@app.route('/v1/')
@jsonify
def root():
    return {
        'tournaments': url_for('tournaments', _external=True),
        'players': url_for('players', _external=True),
        'matches': url_for('matches', _external=True),
    }


@app.route('/v1/tournaments/', methods=['GET', 'POST'])
def tournaments():
    if request.method == 'GET':
        return list_view(simple_filter(models.Tournament, models.Tournament.query))
    if request.method == 'POST':
        return create_tournament()


def create_tournament():
    t = models.Tournament()
    models.db.session.add(t)
    models.db.session.commit()
    return t.href, 201


@app.route('/v1/tournaments/<int:tournament_id>')
@jsonify
def tournament(tournament_id):
    return data(models.Tournament.query.filter(models.Tournament.id == tournament_id).one())


@app.route('/v1/matches/', methods=['GET', 'POST'])
def matches():
    if request.method == 'GET':
        return list_view(simple_filter(models.Match, models.Match.query))
    if request.method == 'POST':
        return create_match()


@app.route('/v1/matches/<int:match_id>', methods=['GET'])
@jsonify
def match(match_id):
    m = models.Match.query.filter(models.Match.id == match_id).one()
    if request.method == 'GET':
        return data(m)


@app.route('/v1/players/', methods=['GET', 'POST'])
def players():
    if request.method == 'GET':
        return list_view(simple_filter(models.Player, models.Player.query))
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


def create_match():
    m = models.Match()
    models.db.session.add(m)
    models.db.session.commit()
    return m.href, 201


@app.route('/v1/players/<int:player_id>')
@jsonify
def player(player_id):
    return data(get_player(player_id))


def get_player(id):
    return models.Player.query.filter(models.Player.id == id).one()


if __name__ == '__main__':
    app.run(debug=True)
