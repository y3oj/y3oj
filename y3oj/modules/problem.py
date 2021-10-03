from y3oj.utils.render import render_markdown_blocks
import yaml
from os import path

from y3oj import db
from y3oj.models import Problem
from y3oj.utils import dirname, listDir, readFile, render_markdown_blocks


def loadFromLocal():
    folders = filter(path.isdir, listDir(path.join(dirname, 'data',
                                                   'problem')))
    db.session.query(Problem).delete()

    for folder in folders:
        args = yaml.load(readFile(path.join(folder, 'config.yml')),
                         Loader=yaml.SafeLoader)
        element = Problem(id=path.basename(folder),
                          key=int(args['key']),
                          title=args['title'])
        # config
        del args['key']
        del args['title']
        element.config = args
        # content
        if path.exists(path.join(folder, 'statement.md')):
            plaintext = readFile(path.join(folder, 'statement.md'))
            element.content = render_markdown_blocks(plaintext)
        db.session.add(element)

    db.session.commit()