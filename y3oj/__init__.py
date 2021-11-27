from flask import Flask

__all__ = [
    'app', 'config', 'db', 'loader', 'judger', 'logger', 'login_manager'
]

from .autoload.logger import logger
from .autoload.config import config

app = Flask(__name__, static_url_path='/assets')
app.secret_key = config.secret_key

from .autoload.db import db
from .autoload.judger import judger
from .models import *
from .autoload.login_manager import login_manager
from .autoload.loader import Loader as loader
from .routes import *