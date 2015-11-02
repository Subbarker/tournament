from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
from tournament import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _players = db.relationship('Player', secondary='tournament_players', backref='_tournaments')
    _matches = db.relationship('Match', backref='_tournament')

    @property
    def href(self):
        return url_for('tournament', tournament_id=self.id, _external=True)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    @property
    def href(self):
        return url_for('player', player_id=self.id, _external=True)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.ForeignKey(Tournament.id))
    round_number = db.Column(db.Integer)
    player_1_id = db.Column(db.ForeignKey(Player.id))
    player_2_id = db.Column(db.ForeignKey(Player.id))
    player_1_wins = db.Column(db.Integer)
    player_2_wins = db.Column(db.Integer)
    ties = db.Column(db.Integer)

    _player_1 = db.relationship(Player, primaryjoin=player_1_id == Player.id, backref='matches')
    _player_2 = db.relationship(Player, primaryjoin=player_2_id == Player.id)

    @property
    def href(self):
        return url_for('match', match_id=self.id, _external=True)


tournament_players = db.Table('tournament_players', db.metadata,
    db.Column('tournament_id', db.ForeignKey('tournament.id')),
    db.Column('player_id', db.ForeignKey('player.id'))
)
