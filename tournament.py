from flask import Flask, request, url_for
from sqlalchemy.orm.exc import NoResultFound
import models
from tools import jsonify, data

app = Flask(__name__)


@app.before_first_request
def setup():
    models.db.create_all()


@app.route('/v1/')
def hello_world():
    return 'Hello World!'


@app.route('/v1/tournaments/', methods=['GET', 'POST'])
def tournaments():
    if request.method == 'POST':
        return create_tournament()

    if request.method == 'GET':
        return get_tournaments()


@jsonify
def get_tournaments():
    return {'content': [url_for('tournament', tournament_id=t.id, _external=True) for t in models.Tournament.query]}


def create_tournament():
    t = models.Tournament()
    models.db.session.add(t)
    models.db.session.commit()
    return url_for('tournament', tournament_id=t.id, _external=True), 201


@app.route('/v1/tournaments/<int:tournament_id>', methods=['GET'])
@jsonify
def tournament(tournament_id):
    try:
        t = models.Tournament.query.filter(models.Tournament.id == tournament_id).one()
    except NoResultFound:
        return {'error': 'does not exist'}, 404

    if request.method == 'GET':
        return data(t)


if __name__ == '__main__':
    app.run(debug=True)

