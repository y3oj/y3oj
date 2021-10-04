from y3oj import app, db
from y3oj.models import Submission
from y3oj.utils import render_template, to_mixin


@app.route('/submission')
def list_submission():
    submissions = db.session \
        .query(Submission) \
        .order_by(Submission.id.desc()) \
        .all()
    return render_template('submission/index.html',
                           submissions=map(to_mixin, submissions))
