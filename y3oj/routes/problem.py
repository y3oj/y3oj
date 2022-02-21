import os
from flask import g, request, redirect, url_for, send_from_directory
from wtforms import TextAreaField, SubmitField
from flask_wtf import FlaskForm
from flask_login import current_user, login_required

from y3oj import app, db, config
from y3oj.utils import render_template, to_mixin
from y3oj.models import Problem
from y3oj.modules.submission import submit_code, query_problem_submissions_by_id
from y3oj.routes.decorater import problem_checker, submit_authority_required


@app.route('/problem')
def route_problem_index():
    pagination = db.session \
        .query(Problem) \
        .paginate( \
            page=int(request.args.get("page", 1)), \
            per_page=int(config.per_page.problem))
    return render_template('problem/index.html',
                           pagination=pagination,
                           problems=pagination.items)


@app.route('/problem/<id>')
@problem_checker
def route_problem(id):
    return render_template('problem/problem.html', problem=g.problem)

@app.route('/problem/<id>/print')
@problem_checker
def route_problem_print(id):
    return render_template('problem/print.html', problem=g.problem)


@app.route('/problem/<id>/submit', methods=['GET', 'POST'])
@submit_authority_required
@login_required
@problem_checker
def route_problem_submit(id):
    class ProblemSubmitForm(FlaskForm):
        code = TextAreaField('代码')
        submit = SubmitField('提交')

    form = ProblemSubmitForm()
    if form.validate_on_submit():
        submit_code(user=current_user,
                    problem=g.problem,
                    code=request.form['code'])
        return redirect(url_for('route_problem_submission', id=id))
    return render_template('problem/submit.html', problem=g.problem, form=form)


@app.route('/problem/<id>/submission')
@problem_checker
def route_problem_submission(id):
    pagination = query_problem_submissions_by_id(id).paginate(
        page=int(request.args.get("page", 1)),
        per_page=int(config.per_page.submission))
    return render_template('problem/submission.html',
                           problem=g.problem,
                           pagination=pagination,
                           submissions=map(to_mixin, pagination.items))


@app.route('/problem/<id>/assets/<path:path>')
@problem_checker
def route_problem_assets(id, path):
    return send_from_directory(
        os.path.join('..', 'data', 'problem', id, 'assets'), path)
