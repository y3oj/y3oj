from flask import jsonify, request
from flask_login import login_required

from y3oj import app
from y3oj.routes.decorater import manage_authority_required
from y3oj.modules.submission import get_submission, rejudge_submission


def execfunc(callable):
    try:
        callable()
        return jsonify({'code': 0})
    except BaseException as e:
        return jsonify({'code': -1, 'error': str(e)})


def exception(code, message):
    return jsonify({'code': int(code), 'message': message})


@app.route('/api/rejudge-submission', methods=['POST'])
@manage_authority_required
@login_required
def api_rejudge_submission():
    id = request.form['id']

    submission = get_submission(id)
    if submission is None:
        return exception(1, 'No such submission')

    return execfunc(lambda: rejudge_submission(id))
