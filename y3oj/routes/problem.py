from flask import g, request, redirect, url_for
from wtforms import TextAreaField, SubmitField
from flask_wtf import FlaskForm
from flask_login import current_user, login_required

from y3oj import app, db
from y3oj.utils import render_template, to_mixin
from y3oj.models import Problem, Submission
from y3oj.modules.submission import submit_code
from y3oj.routes.decorater import problem_checker, submit_authority_required


@app.route('/problem')
def route_problem_index():
    problems = db.session.query(Problem)
    return render_template('problem/index.html', problems=problems)


@app.route('/problem/<id>')
@problem_checker
def route_problem(id):
    return render_template('problem/problem.html', problem=g.problem)


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
    submissions = db.session \
        .query(Submission) \
        .filter_by(problem=id) \
        .order_by(Submission.id.desc()) \
        .all()
    return render_template('problem/submission.html',
                           problem=g.problem,
                           submissions=map(to_mixin, submissions))
