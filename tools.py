from functools import wraps
import flask


def jsonify(func):
    @wraps(func)
    def jsonified(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, tuple):
            return flask.jsonify(result[0]), result[1]
        return flask.jsonify(result)

    return jsonified


def data(sqla_obj):
    return {col: getattr(sqla_obj, col) for col in type(sqla_obj).accessible_columns}
