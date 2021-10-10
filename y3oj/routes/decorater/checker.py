from functools import wraps
from flask import g, abort

from y3oj.modules.user import get_user
from y3oj.modules.problem import get_problem
from y3oj.modules.submission import get_submission


def user_checker(f, attr='id'):
    @wraps(f)
    def decorated_function(**kwargs):
        id = kwargs[attr]
        g.user = get_user(id)
        if g.user is None:
            abort(404)
        return f(id)

    return decorated_function


def problem_checker(f, attr='id'):
    @wraps(f)
    def decorated_function(**kwargs):
        id = kwargs[attr]
        g.problem = get_problem(id)
        if g.problem is None:
            abort(404)
        return f(id)

    return decorated_function


def submission_checker(f, attr='id'):
    @wraps(f)
    def decorated_function(**kwargs):
        id = kwargs[attr]
        g.submission = get_submission(id)
        if g.submission is None:
            abort(404)
        return f(id)

    return decorated_function
