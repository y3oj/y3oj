from flask import request
from flask_login import login_required

from y3oj import app, db
from y3oj.routes.api.utils import execfunc
from y3oj.routes.decorater import root_authority_required


@app.route('/api/action/exec-sql', methods=['POST'])
@root_authority_required
@login_required
def api_action_exec_sql():
    command = request.form['command']
    
    def execute():
        resultProxy = db.session.execute(command)
        if resultProxy.returns_rows:
            return resultProxy.fetchall()
        else:
            return 'executed.'

    return execfunc(execute)