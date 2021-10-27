from flask import g, request

from y3oj import app, db, config
from y3oj.models import Submission
from y3oj.utils import render_template, to_mixin
from y3oj.routes.decorater import submission_checker


@app.route('/submission')
def route_submission_index():
    pagination = db.session \
        .query(Submission) \
        .order_by(Submission.id.desc()) \
        .paginate( \
            page=int(request.args.get("page", 1)), \
            per_page=int(config.per_page.submission))
    return render_template('submission/index.html',
                           pagination=pagination,
                           submissions=map(to_mixin, pagination.items))


@app.route('/submission/<id>')
@submission_checker
def route_submission(id):
    return render_template('submission/submission.html',
                           submission=g.submission.get_mixin())
