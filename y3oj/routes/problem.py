from y3oj import app, db
from y3oj.models import Problem
from y3oj.utils import render_template


@app.route('/problem')
def list_problem():
    problems = db.session.query(Problem)
    return render_template('problem/index.html', problems=problems)


@app.route('/problem/<id>')
def get_problem(id):
    problem = db.session.query(Problem).filter_by(id=id).first()
    return render_template('problem/problem.html', problem=problem)
