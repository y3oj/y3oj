import yaml
import sqlalchemy
from os import path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from y3oj import config
from y3oj.utils import dirname, Container

# app
app = Flask(__name__, static_url_path='/assets')

# database
database_uri = config.database.uri
if database_uri == 'default:///sqlite':
    database_uri = 'sqlite:///' + path.join(dirname, 'data', 'main.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
