from flask import abort
from flask_login import current_user, login_required

from y3oj import app, db
from y3oj.utils import render_template
from y3oj.models import User


@app.route('/homework')
@login_required
def route_homework_index():
    homeworks = []
    for _, homework_group in app.homework.items():
        for _, homework in homework_group.items():
            if homework.includes_user(current_user):
                homeworks.append(homework)
    return render_template('homework/index.html', homeworks=homeworks)


@app.route('/homework/<homework_id>/<usergroup_id>')
@login_required
def route_homework(homework_id, usergroup_id):
    if homework_id not in app.homework or \
            usergroup_id not in app.homework[homework_id]:
        return abort(404)
    homework = app.homework[homework_id][usergroup_id]
    if not homework.includes_user(current_user):
        return abort(403)
    statistics = homework.get_statistics()
    return render_template('homework/homework.html',
                           homework=homework,
                           statistics=statistics)
