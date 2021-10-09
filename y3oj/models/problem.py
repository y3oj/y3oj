import json

from y3oj import db, config as app_config


class Problem(db.Model):
    __tablename__ = 'problem'

    id = db.Column(db.String(30), unique=True)
    key = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(60))
    _config = db.Column(db.Unicode(app_config.database.limit.json))
    _statement = db.Column(db.Unicode(app_config.database.limit.json))
    _solution = db.Column(db.Unicode(app_config.database.limit.json))

    @property
    def config(self):
        res = json.loads(self._config)
        for key in app_config.problem.defaults.__dict__:
            if key not in res:
                res[key] = app_config.problem.defaults.__dict__[key]
        return res

    @config.setter
    def config(self, data):
        self._config = json.dumps(data)

    @property
    def statement(self):
        return json.loads(self._statement)

    @statement.setter
    def statement(self, data):
        self._statement = json.dumps(data)

    def __init__(self, id, key, title, statement=[], config={}):
        self.id = id
        self.key = key
        self.title = title
        self.statement = statement
        self.config = config

    def __repr__(self):
        return '<Problem %s>' % self.id
