from flask import request
from flask_login import login_required

from y3oj import app, db
from y3oj.models import User
from y3oj.models.user import new_user_key
from y3oj.routes.api.utils import execfunc
from y3oj.routes.decorater import admin_authority_required


@app.route('/api/user/new', methods=['POST'])
@admin_authority_required
@login_required
def api_user_new():
    def add_user():
        print(request.form)
        user = User(
            id=request.form['id'],
            key=new_user_key(),
            nickname=request.form['nickname'],
            password=request.form['password'],
            realname=request.form['realname'],
        )
        db.session.add(user)
        db.session.commit()

    return execfunc(add_user)