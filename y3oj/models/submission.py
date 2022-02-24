import json
from datetime import datetime

from y3oj import db, config as app_config
from y3oj.utils import Container, strftime
from y3oj.modules.problem import get_problem
from y3oj.modules.user import get_user_by_key


class SubmissionMixin(object):

    def __init__(self, id, user, problem, code, status, time, memory, create_time, details):
        self.id = id
        self.user = get_user_by_key(user)
        self.problem = get_problem(problem)
        self.code = code
        self.status = status
        self.time = time
        self.memory = memory
        self.create_time = strftime(create_time)
        self.details = details
        self.passed_count = 0
        
        for i in range(len(self.details)):
            detail = self.details[i]
            detail['id'] = i + 1
            if 'time' not in detail:
                detail['time'] = self.time
            if detail['time'] == -1:
                detail['memory'] = -1
            if 'memory' not in detail:
                detail['memory'] = self.memory
            if 'status' not in detail:
                detail['status'] = self.status
            self.details[i] = Container(detail)
            
            if detail['status'] == 'Accepted':
                self.passed_count += 1

    def __repr__(self):
        return '<SubmissionMixin %s>' % self.id


class Submission(db.Model):
    __tablename__ = 'submission'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer)
    problem = db.Column(db.String(30))
    code = db.Column(db.Unicode(app_config.database.limit.code))
    status = db.Column(db.String(30))
    time = db.Column(db.Integer)
    memory = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    _details = db.Column(db.Unicode(app_config.database.limit.details))

    # __mapper_args__ = {'order_by': id.desc()}  # deprecated

    @property
    def details(self):
        return json.loads(self._details)

    @details.setter
    def details(self, data):
        self._details = json.dumps(data)

    def get_mixin(self):
        return SubmissionMixin(id=self.id, user=self.user, problem=self.problem, code=self.code, status=self.status, time=self.time, memory=self.memory, create_time=self.create_time, details=self.details)

    def __init__(self, user, problem, code, status='Waiting...', time=0, memory=0, details=[]):
        self.user = user
        self.problem = problem
        self.code = code
        self.status = status
        self.time = time
        self.memory = memory
        self.details = details

    def __repr__(self):
        return '<Submission %s>' % self.id
