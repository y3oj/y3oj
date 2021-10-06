from flask import g, jsonify
from flask_login import login_required

from y3oj import app, db
from y3oj.models import Submission
from y3oj.utils import render_template, to_mixin
from y3oj.modules.submission import rejudge_submission
from y3oj.routes.decorater import submission_checker, manage_authority_required


@app.route('/submission')
def list_submission():
    submissions = db.session \
        .query(Submission) \
        .order_by(Submission.id.desc()) \
        .all()
    return render_template('submission/index.html',
                           submissions=map(to_mixin, submissions))


@app.route('/submission/<id>')
@submission_checker
def get_submission(id):
    return render_template('submission/submission.html',
                           submission=g.submission.get_mixin())


@app.route('/api/rejudge-submission/<id>')
@manage_authority_required
@login_required
@submission_checker
def rejudge_submission_api(id):
    try:
        rejudge_submission(id)
        return jsonify({'code': 0})
    except BaseException as e:
        return jsonify({'code': 1, 'error': str(e)})
