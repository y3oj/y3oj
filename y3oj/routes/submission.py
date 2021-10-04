from flask import g

from y3oj import app, db
from y3oj.models import Submission
from y3oj.utils import render_template, to_mixin
from y3oj.routes.decorater import submission_checker


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
