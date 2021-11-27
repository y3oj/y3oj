import yaml
from os import path

from y3oj import app, db
from y3oj.models import Problem, Homework, UserGroup
from y3oj.models.homework import HomeworkInitError
from y3oj.utils import dirname, listDir, readFile, basename, render_markdown_blocks


class Loader:
    @staticmethod
    def problem():
        summary = []
        folders = filter(path.isdir,
                         listDir(path.join(dirname, 'data', 'problem')))
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
                prob.statement = render_markdown_blocks(plaintext,
                                                        anti_xss=False)
            summary.append(dict(id=prob.id, key=prob.key, title=prob.title))
            db.session.add(prob)

        db.session.commit()
        return summary

    @staticmethod
    def usergroup():
        filedirs = listDir(path.join(dirname, 'data', 'usergroup'))
        usergroup = {}
        for filedir in filedirs:
            data = yaml.load(readFile(filedir), Loader=yaml.SafeLoader)
            id = basename(filedir)
            usergroup[id] = UserGroup(id, data['name'], data['user'])
        app.usergroup = usergroup

    @staticmethod
    def homework():
        assert app.usergroup
        filedirs = listDir(path.join(dirname, 'data', 'homework'))
        homework = {}
        for filedir in filedirs:
            data = yaml.load(readFile(filedir), Loader=yaml.SafeLoader)
            id = basename(filedir)
            current = {}
            for usergroup in data['usergroup']:
                if usergroup not in app.usergroup:
                    raise HomeworkInitError('作业中的用户组不存在')
                usergroup = app.usergroup[usergroup]
                current[usergroup] = Homework(id, data['name'],
                                              data['description'], usergroup,
                                              data['problem'])
            homework[id] = current
        app.homework = homework

    @staticmethod
    def all():
        Loader.problem()
        Loader.usergroup()
        Loader.homework()
