from flask import Flask

__all__ = ['app', 'config', 'db', 'judger', 'login_manager']

from .autoload.config import config

app = Flask(__name__, static_url_path='/assets')
app.secret_key = config.secret_key

from .autoload.db import db
from .autoload.judger import judger
from .models import *
from .autoload.login_manager import login_manager
from .routes import *
