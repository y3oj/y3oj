import json

from y3oj import db, config as app_config
from flask_login import UserMixin as UserMixinBase, AnonymousUserMixin as AnonymousUserMixinBase


class UserMixin(UserMixinBase):
    @property
    def displayName(self):
        return self.nickname or self.id

    def get_model(self):
        return User(id=self.id,
                    key=self.key,
                    nickname=self.nickname,
                    password=self.password,
                    settings=self.settings,
                    authority=self.authority)

    def __init__(self, id, key, nickname, password, settings, authority):
        self.id = id or ''
        self.key = key or 0
        self.nickname = nickname or ''
        self.password = password or ''
        self.settings = settings or {}
        self.authority = authority or 0


class AnonymousUserMixin(AnonymousUserMixinBase):
    pass


class User(db.Model):
    __hash__ = object.__hash__
    id = db.Column(db.String(30), unique=True)
    key = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.Unicode(60), unique=True)
    password = db.Column(db.String(32))  # md5 salt hashed
    _settings = db.Column(db.Unicode(app_config.database.max_json_length))
    authority = db.Column(db.Integer)

    @property
    def settings(self):
        return json.loads(self._settings)

    @settings.setter
    def settings(self, data):
        self._settings = json.dumps(data)

    def get_mixin(self):
        return UserMixin(id=self.id,
                         key=self.key,
                         nickname=self.nickname,
                         password=self.password,
                         settings=self.settings,
                         authority=self.authority)

    def __init__(self, id, key, nickname, password, settings, authority):
        self.id = id or ''
        self.key = key or 0
        self.nickname = nickname or ''
        self.password = password or ''
        self.settings = settings or {}
        self.authority = authority or 0

    def __repr__(self):
        return '<User %s>' % self.id
