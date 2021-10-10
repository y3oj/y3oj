from os import path
from flask_sqlalchemy import SQLAlchemy

from y3oj import app, config
from y3oj.utils import dirname

database_uri = config.database.uri
if database_uri == 'default:///sqlite':
    database_uri = 'sqlite:///' + path.join(dirname, 'data', 'main.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)