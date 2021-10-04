import json

from y3oj import db, config as app_config
from y3oj.modules.problem import get_problem
from y3oj.modules.user import get_user_by_key


class SubmissionMixin(object):
    def __init__(self, id, user, problem, code, status, details):
        self.id = id
        self.user = get_user_by_key(user)
        self.problem = get_problem(problem)
        self.code = code
        self.status = status
        self.details = details
        print('[submission-mixin]', self.user, self.problem)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer)
    problem = db.Column(db.String(30))
    code = db.Column(db.Unicode(app_config.database.max_code_length))
    status = db.Column(db.String(30))
    _details = db.Column(db.Unicode(app_config.database.max_details_length))

    # __mapper_args__ = {'order_by': id.desc()}  # deprecated

    @property
    def details(self):
        return json.loads(self._details)

    @details.setter
    def details(self, data):
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
        print(
            user,
            problem,
        )
        self.user = user
        self.problem = problem
        self.code = code
        self.status = status
        self.details = details

    def __repr__(self):
        return '<Submission %s>' % self.id
