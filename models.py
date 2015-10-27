from flask.ext.sqlalchemy import SQLAlchemy
from tournament import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


class Match(db.Model):
    round_id = db.Column(db.Integer, primary_key=True)
    player_1_id = db.Column(db.Integer, primary_key=True)
    player_2_id = db.Column(db.Integer, primary_key=True)


class Round(db.Model):
    tournament_id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.String(80), primary_key=True)


