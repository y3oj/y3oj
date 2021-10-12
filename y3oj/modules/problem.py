import yaml
from os import path

from y3oj import db
from y3oj.models import Problem
from y3oj.utils import dirname, listDir, readFile, render_markdown_blocks


def get_problem(id: str):
    return db.session.query(Problem).filter_by(id=id).first()


def load_problems():
    summary = []
    folders = filter(path.isdir, listDir(path.join(dirname, 'data',
                                                   'problem')))
    db.session.query(Problem).delete()

    for folder in folders:
        args = yaml.load(readFile(path.join(folder, 'config.yml')),
                         Loader=yaml.SafeLoader)
        prob = Problem(id=path.basename(folder),
                       key=int(args['key']),
                       title=args['title'])
        # config
        del args['key']
        del args['title']
        prob.config = args
        # statement
        if path.exists(path.join(folder, 'statement.md')):
            plaintext = readFile(path.join(folder, 'statement.md'))
            prob.statement = render_markdown_blocks(plaintext, anti_xss=False)
        summary.append(dict(id=prob.id, key=prob.key, title=prob.title))
        db.session.add(prob)

    db.session.commit()
    return summary
