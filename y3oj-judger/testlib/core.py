import json
import subprocess
from os import path

from .utils import *
from .pipe import InputPipe, OutputPipe


class Config:
    def __init__(self):
        self.problem_name = 'noname'
        self.solution_path = path.abspath(
            path.join(path.dirname(__file__), 'sol.py'))


class Task:
    def __getattr__(self, name):
        if name.startswith('_') and not name.endswith('_'):
            raise KeyError('private attr')
        if name in dir(self):
            return getattr(self, name)
        elif name in dir(self.stdin):
            return getattr(self.stdin, name)
        elif name in dir(self.stdout):
            return getattr(self.stdout, name)
        else:
            raise KeyError()

    def __init__(self, task_id, testlib_config):
        self.id = task_id
        self.testlib = testlib_config
        self.stdin = None
        self.stdout = None


config = Config()
judgers = []


def register_judger(judger, tasks=[]):
    for task in tasks:
        while len(judgers) <= task:
            judgers.append(None)
        judgers[task] = judger


def run_task(judger, task_id):
    res = None
    task = Task(task_id=task_id, testlib_config=config)
    ps = subprocess.Popen(['python', config.solution_path],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=None)
    task.stdin = InputPipe(ps.stdin)
    task.stdout = OutputPipe(ps.stdout)
    res = judger(task)
    ps.wait()
    return res


def run(tasks=None):
    if tasks is None:
        tasks = range(0, len(judgers))
    res = []
    for task in tasks:
        try:
            data = run_task(judgers[task], task_id=task)
            res.append(data)
        except Exception as e:
            res.append(dict(status='Runtime Error', message=str(e)))
            raise e
    print('[SUCCESS]', json.dumps(res))
