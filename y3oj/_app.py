from flask import Flask

from y3oj import config

app = Flask(__name__, static_url_path='/assets')
app.secret_key = config.secret_key