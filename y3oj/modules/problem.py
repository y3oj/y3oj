import yaml
from os import path

from y3oj import db
from y3oj.models import Problem
from y3oj.utils import dirname, listDir, readFile, render_markdown_blocks


def get_problem(id: str):
    return db.session.query(Problem).filter_by(id=id).first()


def load_problems():
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
        # statement
        if path.exists(path.join(folder, 'statement.md')):
            plaintext = readFile(path.join(folder, 'statement.md'))
            element.statement = render_markdown_blocks(plaintext)
        db.session.add(element)

    db.session.commit()
