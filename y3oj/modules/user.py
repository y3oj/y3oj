from y3oj import db
from y3oj.models import User


def getUserById(id):
    res = db.session.query(User).filter_by(id=id).all()
    return res[0] if len(res) else None
