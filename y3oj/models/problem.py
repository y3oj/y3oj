import json

from y3oj import db, config as app_config
from y3oj.utils import render_markdown_blocks


class Problem(db.Model):
    id = db.Column(db.String(30), unique=True)
    rank = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(60))
    _config = db.Column(db.Unicode(app_config.database.max_json_length))
    _content = db.Column(db.Unicode(app_config.database.max_json_length))

    @property
    def config(self):
        return json.loads(self._config)

    @config.setter
    def config(self, jsondata):
        self._config = json.dumps(jsondata)

    @property
    def content(self):
        return json.loads(self._content)

    @content.setter
    def content(self, data):
        if data.startsWith('{') or data.startsWith('['):  # json data
            self._content = json.dumps(data)
        else:
            self._content = render_markdown_blocks(data)

    def __init__(self, id='', rank=0, title='', content=[], config={}):
        self.id = id
        self.rank = rank
        self.title = title
        self.config = config
        self.content = content

    def __repr__(self):
        return '<Problem %s>' % self.id
