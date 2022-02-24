import traceback
from flask import jsonify

from y3oj import logger

execfunc_logger = logger.module('execfunc')


def execfunc(callable, *args, **kwargs):
    try:
        res = callable(*args, **kwargs)
        if res is None:
            return jsonify({'code': 0})
        else:
            return jsonify({'code': 0, 'result': res})
    except BaseException:
        execfunc_logger.warn(traceback.format_exc())
        return jsonify({'code': -1, 'message': traceback.format_exc()})


def exception(code, message):
    return jsonify({'code': int(code), 'message': message})