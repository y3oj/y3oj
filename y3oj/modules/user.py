from y3oj import db
from y3oj.models import User


def get_user(id):
    res = db.session.query(User).filter_by(id=id).all()
    return res[0] if len(res) else None


def get_user_by_key(key):
    res = db.session.query(User).filter_by(key=key).all()
    return res[0] if len(res) else None
