import json
from flask import request, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import login_required
from wtforms import TextField, TextAreaField, SubmitField

from y3oj import app, db
from y3oj.models import Problem
from y3oj.utils import render_template
from y3oj.routes.decorater import submit_authority_required


@app.route('/problem')
def list_problem():
    problems = db.session.query(Problem)
    return render_template('problem/index.html', problems=problems)


@app.route('/problem/<id>')
def get_problem(id):
    problem = db.session.query(Problem).filter_by(id=id).first()
    return render_template('problem/problem.html', problem=problem)


class ProblemSubmitForm(FlaskForm):
    code = TextAreaField('代码')
    submit = SubmitField('提交')


@app.route('/problem/<id>/submit', methods=['GET', 'POST'])
@submit_authority_required
@login_required
def submit_problem(id):
    form = ProblemSubmitForm()
    problem = db.session.query(Problem).filter_by(id=id).first()
    if form.validate_on_submit():
        code = request.form['code'] \
            .replace('\r\n', '\n') \
            .replace('\r', '\n')
        print('submit code:', json.dumps({'code': code}))
        return redirect(url_for('get_problem', id=id))
    return render_template('problem/submit.html', problem=problem, form=form)
