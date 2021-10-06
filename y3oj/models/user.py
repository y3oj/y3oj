import json

from y3oj import db, config as app_config
from flask_login import UserMixin as UserMixinBase, AnonymousUserMixin as AnonymousUserMixinBase


class UserMixin(UserMixinBase):
    @property
    def displayName(self):
        return self.nickname or self.id

    @property
    def has_submit_authority(self):
        return self.authority >= 2

    @property
    def has_manage_authority(self):
        return self.authority >= 3

    @property
    def has_admin_authority(self):
        return self.authority >= 4

    @property
    def has_root_authority(self):
        return self.authority >= 5

    def get_model(self):
        return User(id=self.id,
                    key=self.key,
                    nickname=self.nickname,
                    password=self.password,
                    settings=self.settings,
                    authority=self.authority)
    
    def __eq__(self, other):
        return self.key == other.key

    def __init__(self, id, key, nickname, password, settings, authority):
        self.id = id
        self.key = key
        self.nickname = nickname
        self.password = password
        self.settings = settings
        self.authority = authority


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
        self.id = id
        self.key = key
        self.nickname = nickname
        self.password = password
        self.settings = settings
        self.authority = authority

    def __repr__(self):
        return '<User %s>' % self.id
