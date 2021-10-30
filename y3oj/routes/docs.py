import os
from os import path
from flask import abort, send_from_directory

from y3oj import app
from y3oj.utils import dirname, readFile, render_markdown, path_join, render_template

docs_root = path_join(dirname, 'y3oj-docs')


@app.route('/docs')
def route_docs_index():
    return render_template(
        'docs/article.html',
        **render_markdown(readFile(path_join(docs_root, 'README.md')),
                          anti_xss=False,
                          frontmatter=True))


@app.route('/docs/<path:path>')
def route_docs(path):
    local_path = path_join(docs_root, path + '.md')
    basename, extname = os.path.splitext(os.path.basename(local_path))
    if path.startswith('.'):
        return abort(400)
    if not os.path.exists(local_path):
        return abort(404)

    return render_template('docs/article.html',
                           title=basename,
                           **render_markdown(readFile(local_path),
                                             anti_xss=False,
                                             frontmatter=True))


@app.route('/docs/assets/<path:path>')
def route_docs_assets(path):
    return send_from_directory(os.path.join(docs_root, 'assets'), path)
