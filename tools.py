from functools import wraps
import flask
from flask import request
from sqlalchemy.exc import InvalidRequestError
import models


def jsonify(func):
    @wraps(func)
    def jsonified(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, tuple):
            return flask.jsonify(result[0]), result[1]
        return flask.jsonify(result)

    return jsonified


def data(sqla_obj):
    return {k: getattr(sqla_obj, k) for k in vars(type(sqla_obj)) if not k.startswith('_')}


@jsonify
def list_view(q):
    return {'content': [o.href for o in q]}


def simple_filter(model, q):
    for k, v in flask.request.args.items():
        q = q.filter(getattr(model, k) == v)
    return q


def resource_list(model):
    if request.method == 'GET':
        return list_view(simple_filter(model, model.query))
    if request.method == 'POST':
        return create_resource(model)


def create_resource(model):
    m = model(**(request.json or {}))
    models.db.session.add(m)
    try:
        models.db.session.commit()
    except InvalidRequestError:
        models.db.session.rollback()
        return {'error': 'conflict'}, 409
    return m.href, 201