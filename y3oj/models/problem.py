import json

from y3oj import db, config as app_config


class Problem(db.Model):
    id = db.Column(db.String(30), unique=True)
    key = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(60))
    _config = db.Column(db.Unicode(app_config.database.max_json_length))
    _content = db.Column(db.Unicode(app_config.database.max_json_length))

    @property
    def config(self):
        return json.loads(self._config)

    @config.setter
    def config(self, data):
        self._config = json.dumps(data)

    @property
    def content(self):
        return json.loads(self._content)

    @content.setter
    def content(self, data):
        self._content = json.dumps(data)

    def __init__(self, id='', key=0, title='', content=[], config={}):
        self.id = id
        self.key = key
        self.title = title
        self.config = config
        self.content = content

    def __repr__(self):
        return '<Problem %s>' % self.id
