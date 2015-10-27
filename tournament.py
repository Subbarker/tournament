from flask import Flask, request
from models import db, Tournament

app = Flask(__name__)


@app.before_first_request
def setup():
    db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/tournaments/', methods=['GET', 'POST'])
def tournaments():
    if request.method == 'POST':
        t = Tournament()
        db.session.add(t)
        db.session.commit()
        return str(t.id), 201
    else:
        return Tournament.query


@app.route('/tournaments/<id>', methods=['GET', 'DELETE'])
def tournament(id):
    if request.method == 'DELETE':
        t = Tournament()
        db.session.add(t)
        db.session.commit()
        return str(t.id), 201
    else:
        return 'foo', 200


if __name__ == '__main__':
    app.run(debug=True)

