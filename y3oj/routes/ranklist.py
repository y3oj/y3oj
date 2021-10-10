# -*- coding: UTF-8 -*-

from y3oj import app, db
from y3oj.utils import render_template
from y3oj.models import User


@app.route('/ranklist')
def route_ranklist():
    userlist = db.session.query(User).all()
    return render_template('ranklist/index.html', userlist=userlist)
