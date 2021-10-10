from y3oj import db
from y3oj.models import User


def get_user(id: str):
    return db.session.query(User).filter_by(id=id).first()


def get_user_by_key(key: int):
    return db.session.query(User).filter_by(key=key).first()
    