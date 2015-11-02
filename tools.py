from functools import wraps
import flask
from sqlalchemy.orm.state import InstanceState


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
