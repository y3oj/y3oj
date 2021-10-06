from flask_login import LoginManager

from y3oj import app, db
from y3oj.models import User

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    global db
    res = db.session.query(User).filter_by(id=user_id).all()
    return res[0].get_mixin() if len(res) else None