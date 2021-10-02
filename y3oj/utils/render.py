import re
import flask


def render_markdown(source):
    import markdown2
    if isinstance(source, list):
        return map(render_markdown, source)
    elif not isinstance(source, str):
        raise TypeError('[y3oj] markdown source should be string')
    return markdown2.markdown(source,
                              extras=[
                                  'code-friendly', 'fenced-code-blocks',
                                  'header-ids', 'nofollow', 'strike', 'tables',
                                  'task_list'
                              ])


def render_markdown_blocks(source):
    from y3oj.utils import Container
    marked = render_markdown(source)
    blocks = []
    for line in re.split(r'<h1.*?>', marked):
        splited = line.split(r'</h1>')
        if len(splited) == 1:
            splited.insert(0, '')
        title = splited[0].strip()
        content = splited[1].strip()
        if not title and not content:
            continue
        blocks.append({
            'title': title,
            'content': content,
        })
    return blocks


def render_template(path, **data):
    from y3oj import config

    def assets(uri):
        return '/assets' + uri

    render = flask.render_template
    return render(path, assets=assets, config=config, **data)