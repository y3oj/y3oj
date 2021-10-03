from functools import wraps
from flask_login import current_user
from flask import abort, redirect, url_for


def authority_required(f, min_authority):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return redirect(url_for('login'))
        if current_user.authority < min_authority:
            return abort(400, 'Permission denied.')
        return f(*args, **kwargs)

    return decorated_function


def submit_authority_required(f):
    return authority_required(f, 2)


def manage_authority_required(f):
    return authority_required(f, 3)


def admin_authority_required(f):
    return authority_required(f, 4)


def root_authority_required(f):
    return authority_required(f, 5)
