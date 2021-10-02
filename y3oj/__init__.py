from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from y3oj.utils import dirname

__all__ = ['app', 'login_manager', 'db', 'config']

# config
from .modules.config import config


# app
def init_app():
    global app
    app = Flask(__name__, static_url_path='/assets')
    app.secret_key = config.secret_key


init_app()


# db
def init_database():
    global app, db
    database_uri = config.database.uri
    if database_uri == 'default:///sqlite':
        database_uri = 'sqlite:///' + path.join(dirname, 'data', 'main.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)


init_database()

# models
from .models import *


# login_manager
def init_login():
    global app, login_manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        global db
        res = db.session.query(User).filter_by(id=user_id).all()
        return res[0].get_mixin() if len(res) else None


init_login()

# routes
from .routes import *
