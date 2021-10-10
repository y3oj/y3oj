from flask_login import login_required

from y3oj import app, db
from y3oj.utils import render_template
from y3oj.models import User, Problem, Submission
from y3oj.routes.decorater import manage_authority_required

admin_routes = {
    'submission':
    dict(
        name='提交记录',
        icon='storage',
        icon_color='teal',
        links={
            'rejudge-submission': '重测提交记录',
        },
    ),
}


@app.route('/admin')
@manage_authority_required
@login_required
def route_admin_index():
    user_count = db.session.query(User).count()
    problem_count = db.session.query(Problem).count()
    submission_count = db.session.query(Submission).count()
    return render_template(
        'admin/index.html',
        routes=admin_routes,
        user_count=user_count,
        problem_count=problem_count,
        submission_count=submission_count,
    )
