import os
from os import path
from y3oj.utils.file import readFile
from flask import abort

from y3oj import app
from y3oj.utils import dirname, render_markdown, path_join, render_template

docs_root = path_join(dirname, './y3oj/docs')


@app.route('/docs/<path:path>')
def route_docs(path):
    local_path = path_join(docs_root, path + '.md')
    if path.startswith('.'):
        return abort(400)
    if not os.path.exists(local_path):
        return abort(404)

    print('render', render_markdown(readFile(local_path), frontmatter=True))
    return render_template(
        'docs/article.html',
        **render_markdown(readFile(local_path), frontmatter=True))
