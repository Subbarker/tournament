from flask import Flask, request, url_for

import models
from tools import jsonify, data, resource_list, modify_resource

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


@app.route('/v1/tournaments/<id>')
def tournament(id):
    return data(models.Tournament.query.filter(models.Tournament.id == id).one())


@app.route('/v1/matches/', methods=['GET', 'POST'])
def matches():
    return resource_list(models.Match)


@app.route('/v1/matches/<id>', methods=['GET', 'PUT'])
def match(id):
    m = models.Match.query.filter(models.Match.id == id).one()
    if request.method == 'GET':
        return data(m)
    if request.method == 'PUT':
        return modify_resource(m)


@app.route('/v1/players/', methods=['GET', 'POST'])
def players():
    return resource_list(models.Player)


@app.route('/v1/players/<id>')
def player(id):
    return data(models.Player.query.filter(models.Player.id == id).one())


if __name__ == '__main__':
    app.run(debug=True)
