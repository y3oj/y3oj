from y3oj import app, db
from y3oj.utils import render_template
from y3oj.models import Submission


@app.route('/submission')
def list_submission():
    submissions = db.session.query(Submission).all()
    return render_template('submission/index.html', submissions=submissions)
