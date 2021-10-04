from functools import wraps
from flask_login import current_user
from flask import g, abort, redirect, url_for

from y3oj import db
from y3oj.models import Problem
from y3oj.modules.problem import get_problem
from y3oj.modules.submission import get_submission


def problem_checker(f, name='id'):
    @wraps(f)
    def decorated_function(**kwargs):
        id = kwargs[name]
        g.problem = get_problem(id)
        if g.problem is None:
            abort(404)
        return f(id)

    return decorated_function


def submission_checker(f, name='id'):
    @wraps(f)
    def decorated_function(**kwargs):
        id = kwargs[name]
        g.submission = get_submission(id)
        if g.submission is None:
            abort(404)
        return f(id)

    return decorated_function
