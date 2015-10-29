from flask.ext.sqlalchemy import SQLAlchemy
from tournament import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    accessible_columns = {'id'}


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


class Match(db.Model):
    round_id = db.Column(db.Integer, primary_key=True)
    _player_1_id = db.Column(db.ForeignKey(Player.id), primary_key=True)
    _player_2_id = db.Column(db.ForeignKey(Player.id), primary_key=True)
    player_1_wins = db.Column(db.Integer)
    player_2_wins = db.Column(db.Integer)
    ties = db.Column(db.Integer)

    player_1 = db.relationship(Player, primaryjoin=_player_1_id == Player.id, backref='matches')
    player_2 = db.relationship(Player, primaryjoin=_player_2_id == Player.id)


class Round(db.Model):
    tournament_id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.String(80), primary_key=True)


