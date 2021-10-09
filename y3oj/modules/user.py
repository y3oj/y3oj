from y3oj import db
from y3oj.models import User


def get_user(id: str):
    res = db.session.query(User).filter_by(id=id).all()
    return res[0] if len(res) else None


def get_user_by_key(key: int):
    res = db.session.query(User).filter_by(key=key).all()
    return res[0] if len(res) else None
