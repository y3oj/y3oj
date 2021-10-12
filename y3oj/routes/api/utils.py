import traceback
from flask import jsonify


def execfunc(callable):
    try:
        res = callable()
        if res is None:
            return jsonify({'code': 0})
        else:
            return jsonify({'code': 0, 'result': res})
    except BaseException:
        return jsonify({'code': -1, 'message': traceback.format_exc()})


def exception(code, message):
    return jsonify({'code': int(code), 'message': message})