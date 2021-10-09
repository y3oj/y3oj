from functools import wraps
from flask_login import current_user
from flask import abort, redirect, url_for

from y3oj.models import SUBMIT_AUTHORITY, MANAGE_AUTHORITY, ADMIN_AUTHORITY, ROOT_AUTHORITY


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
    return authority_required(f, SUBMIT_AUTHORITY)


def manage_authority_required(f):
    return authority_required(f, MANAGE_AUTHORITY)


def admin_authority_required(f):
    return authority_required(f, ADMIN_AUTHORITY)


def root_authority_required(f):
    return authority_required(f, ROOT_AUTHORITY)
