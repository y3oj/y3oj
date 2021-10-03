import json
import random
import subprocess
from os import path

encoding = 'gbk'


class Random:
    def _randint(self, a, b):
        return random.randint(a, b)

    def _randrange(self, a, b, c=None):
        if c is None:
            return random.randrange(a, b)
        else:
            return random.randrange(a, b, c)

    def __getattr__(self, name):
        if ('_' + name) in dir(self):

            def decorator(*args, **kwargs):
                current = random.getstate()
                random.setstate(self.state)
                res = getattr(self, '_' + name)(*args, **kwargs)
                self.state = random.getstate()
                random.setstate(current)
                return res

            return decorator

        else:
            raise KeyError()

    def __init__(self, seed=None):
        current = random.getstate()
        random.seed(seed, version=2)
        self.state = random.getstate()
        random.setstate(current)


class InputPipeError(Exception):
    pass


class OutputPipeError(Exception):
    pass


class InputPipe(object):
    def _send(self, string):
        self.pipe.write(string.encode(encoding))
        self.pipe.flush()

    def send(self, text, end='\n'):
        self._send(text + end)

    def __init__(self, pipe):
        assert pipe.writable()
        self.pipe = pipe
        # print('input', dir(pipe))


class OutputPipe(object):
    def _recv(self):
        self.cache += self.pipe.read1().decode(encoding)

    def _reset_cache(self):
        self.cache = ''
        self.pointer = 0

    def recv(self):
        self._recv()
        res = self.cache[self.pointer:]
        self._reset_cache()
        return res

    def recv_int(self):
        self._recv()
        if self.pointer == len(self.cache):
            raise OutputPipeError('No integers more.')
        res = 0
        while self.pointer < len(self.cache):
            c = self.cache[self.pointer]
            if 48 <= ord(c) and ord(c) <= 57:
                res = res * 10 + int(c)
                self.pointer += 1
            else:
                break
        if self.pointer == len(self.cache):
            self._reset_cache()
        return res

    def __init__(self, pipe):
        assert pipe.readable()
        self.pipe = pipe
        self._reset_cache()
        # print('output', dir(pipe))


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
