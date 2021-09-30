import flask
import markdown2

import y3oj


def render_markdown(source):
    if isinstance(source, list):
        return map(render_markdown, source)
    elif not isinstance(source, str):
        raise TypeError('[y3oj] markdown source should be string')
    return markdown2.markdown(source)


def render_template(path, **data):
    return flask.render_template(path, config=y3oj.config, **data)
