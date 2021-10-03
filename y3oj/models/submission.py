import json

from y3oj import db, config as app_config
from y3oj.modules.user import getUserById
from y3oj.modules.problem import getProblemById


class SubmissionMixin(object):
    def __init__(self, id, user, problem, code, status, details):
        self.id = id
        self.user = getUserById(user)
        self.problem = getProblemById(problem)
        self.code = code
        self.status = status
        self.details = details


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

    def get_mixin(self):
        return SubmissionMixin(id=self.id,
                               user=self.user,
                               problem=self.problem,
                               code=self.code,
                               status=self.status,
                               details=self.details)

    def __init__(self,
                 user,
                 problem,
                 code,
                 status='Waiting...',
                 details=dict(time_cost=0, memory_cost=0, result=[])):
        self.user = user
        self.problem = problem
        self.code = code
        self.status = status
        self.details = details

    def __repr__(self):
        return '<Problem %s>' % self.id
