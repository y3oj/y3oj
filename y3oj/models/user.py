import json

from y3oj import db, config as app_config
from flask_login import UserMixin

SUBMIT_AUTHORITY = 1
MANAGE_AUTHORITY = 2
ADMIN_AUTHORITY = 3
ROOT_AUTHORITY = 4


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __hash__ = object.__hash__

    id = db.Column(db.String(30), unique=True)
    key = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.Unicode(60), unique=True)
    password = db.Column(db.String(32))  # md5 salt hashed
    realname = db.Column(db.Unicode(10))
    authority = db.Column(db.Integer)
    _settings = db.Column(db.Unicode(app_config.database.limit.json))

    @property
    def settings(self):
        return json.loads(self._settings)

    @settings.setter
    def settings(self, data):
        self._settings = json.dumps(data)

    @property
    def displayName(self):
        return self.nickname or self.id

    @property
    def has_submit_authority(self):
        return self.authority >= SUBMIT_AUTHORITY

    @property
    def has_manage_authority(self):
        return self.authority >= MANAGE_AUTHORITY

    @property
    def has_admin_authority(self):
        return self.authority >= ADMIN_AUTHORITY

    @property
    def has_root_authority(self):
        return self.authority >= ROOT_AUTHORITY

    @staticmethod
    def verify_id(id: str):
        if len(id) > 30:
            return '用户 id 过长'
        if id.isdigit():
            return '用户 id 不能全是数字'
        return False

    def __eq__(self, other):
        return isinstance(other, User) and self.key == other.key

    def __init__(self, id, key, nickname, password, realname, authority,
                 settings):
        self.id = id
        self.key = key
        self.nickname = nickname
        self.password = password
        self.realname = realname
        self.authority = authority
        self.settings = settings

    def __repr__(self):
        return '<User %s>' % self.id
