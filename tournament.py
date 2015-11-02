from flask import Flask, request, url_for

import models
from tools import jsonify, data, resource_list

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
    return resource_list(models.Tournament)


@app.route('/v1/tournaments/<int:tournament_id>')
@jsonify
def tournament(tournament_id):
    return data(models.Tournament.query.filter(models.Tournament.id == tournament_id).one())


@app.route('/v1/matches/', methods=['GET', 'POST'])
def matches():
    return resource_list(models.Match)


@app.route('/v1/matches/<int:match_id>', methods=['GET'])
@jsonify
def match(match_id):
    m = models.Match.query.filter(models.Match.id == match_id).one()
    if request.method == 'GET':
        return data(m)


@app.route('/v1/players/', methods=['GET', 'POST'])
def players():
    return resource_list(models.Player)


@app.route('/v1/players/<int:player_id>')
@jsonify
def player(player_id):
    return data(models.Player.query.filter(models.Player.id == player_id).one())


if __name__ == '__main__':
    app.run(debug=True)
