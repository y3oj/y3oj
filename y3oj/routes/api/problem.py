from flask_login import login_required

from y3oj import app, loader
from y3oj.routes.api.utils import execfunc
from y3oj.routes.decorater import admin_authority_required


@app.route('/api/action/reload-problems', methods=['POST'])
@admin_authority_required
@login_required
def api_action_reload_problems():
    return execfunc(loader.problem)