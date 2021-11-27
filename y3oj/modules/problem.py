from y3oj import db
from y3oj.models import Problem


def get_problem(id: str):
    return db.session.query(Problem).filter_by(id=id).first()
