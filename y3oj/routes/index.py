from y3oj import app
from y3oj.utils import render_template


@app.route('/')
def route_index():
    return render_template('index.html')
