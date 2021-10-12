from flask_login import login_required

from y3oj import app, db
from y3oj.utils import render_template
from y3oj.models import User, Problem, Submission
from y3oj.models.user import MANAGE_AUTHORITY, ADMIN_AUTHORITY, ROOT_AUTHORITY
from y3oj.routes.decorater import manage_authority_required, admin_authority_required

admin_routes = {
    'problem':
    dict(
        name='题目',
        icon='book',
        color='deep-orange',
        links={
            'reload-all': dict(name='重载题目', authority=ADMIN_AUTHORITY),
        },
    ),
    'submission':
    dict(
        name='提交记录',
        icon='storage',
        color='teal',
        links={
            'rejudge': dict(name='重测提交记录', authority=MANAGE_AUTHORITY),
        },
    ),
}


@app.route('/admin')
@manage_authority_required
@login_required
def admin_index():
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


@app.route('/admin/problem/reload-all')
@admin_authority_required
@login_required
def admin_problem_reload_all():
    return render_template(
        'admin/postapi.html',
        routes=admin_routes,
        title='重载题目',
        api='/api/action/reload-problems',
        message='重载所有题目，会暂时中断题目服务。请在空闲时段使用。',
        args=dict(),
    )


@app.route('/admin/submission/rejudge')
@manage_authority_required
@login_required
def admin_submission_rejudge():
    return render_template(
        'admin/postapi.html',
        routes=admin_routes,
        title='重测提交记录',
        api='/api/action/rejudge-submission',
        message='重新测评提交记录，建议在题目数据修改或评测服务中断后使用。（功能需要加强）',
        args=dict(id='提交记录 ID'),
    )
