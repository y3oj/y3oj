import json

from y3oj import db, config as app_config


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer)
    problem = db.Column(db.String(30))
    code = db.Column(db.Unicode(app_config.database.max_code_length))
    status = db.Column(db.String(30))
    _details = db.Column(db.Unicode(app_config.database.max_details_length))

    @property
    def details(self):
        return json.loads(self._details)

    @details.setter
    def config(self, data):
        self._details = json.dumps(data)

    def __init__(self, user, problem, code, status, details):
        self.user = user or 0
        self.problem = problem or ''
        self.code = code or ''
        self.status = status or 'Waiting...'
        self.details = details or []

    def __repr__(self):
        return '<Problem %s>' % self.id
