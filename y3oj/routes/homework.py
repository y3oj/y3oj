from flask_login import current_user, login_required

from y3oj import app, db
from y3oj.utils import render_template
from y3oj.models import User


@app.route('/homework')
@login_required
def route_homework():
    homeworks = []
    for _, homework_group in app.homework.items():
        for _, homework in homework_group.items():
            if homework.includes_user(current_user):
                homeworks.append(homework)
    return render_template('homework/index.html', homeworks=homeworks)
