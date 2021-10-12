from flask import request
from flask_login import login_required

from y3oj import app
from y3oj.routes.api.utils import execfunc, exception
from y3oj.routes.decorater import manage_authority_required
from y3oj.modules.submission import get_submission, rejudge_submission


@app.route('/api/action/rejudge-submission', methods=['POST'])
@manage_authority_required
@login_required
def api_action_rejudge_submission():
    id = request.form['id']

    submission = get_submission(id)
    if submission is None:
        return exception(1, 'No such submission')

    return execfunc(lambda: rejudge_submission(id))
