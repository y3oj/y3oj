import functools
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
    user_list = homework.usergroup.user_list
    if not homework.includes_user(current_user):
        return abort(403)

    statistics = homework.get_statistics()
    accepted_number = [0 for _ in range(len(statistics))]
    for i in range(len(statistics)):
        for j in range(len(statistics[i])):
            if statistics[i][j] is not None and \
                    statistics[i][j].status == 'Accepted':
                accepted_number[i] += 1

    def cmp(i, j):
        print('COMPARE', i, j)
        return accepted_number[j] - accepted_number[i] or \
                user_list[i].key - user_list[j].key

    sorted_user_index = [i for i in range(len(user_list))]
    sorted_user_index.sort(key=functools.cmp_to_key(cmp))
    print('SORTED', accepted_number, sorted_user_index)

    return render_template('homework/homework.html',
                           homework=homework,
                           statistics=statistics,
                           accepted_number=accepted_number,
                           user_list=user_list,
                           sorted_user_index=sorted_user_index)
