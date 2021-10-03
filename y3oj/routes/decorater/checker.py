from functools import wraps
from flask_login import current_user
from flask import g, abort, redirect, url_for

from y3oj import db
from y3oj.models import Problem
from y3oj.modules.problem import getProblemById


def problem_checker(f):
    @wraps(f)
    def decorated_function(id):
        g.problem = getProblemById(id)
        if g.problem is None:
            abort(404)
        return f(id)

    return decorated_function
