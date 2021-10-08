import json
import random
import subprocess
from os import path

pipe_encoding = 'gbk'


class BaseResult(Exception):
    pass


class Accepted(BaseResult):
    pass


class WrongAnswer(BaseResult):
    pass


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


class InputPipe(object):
    class InputPipeError(Exception):
        pass

    def _send(self, string):
        self.pipe.write(string.encode(pipe_encoding))
        self.pipe.flush()

    def send(self, text):
        self._send(text)

    def sendline(self, text, end='\n'):
        self._send(text + end)

    def __init__(self, pipe):
        assert pipe.writable()
        self.pipe = pipe
        # print('input', dir(pipe))


class OutputPipe(object):
    class OutputPipeError(Exception):
        pass

    def _reset_cache(self):
        self.cache = ''
        self.pointer = 0

    def _recv(self):
        self.cache = self.pipe.read1().decode(pipe_encoding)
        self.pointer = 0

    def recv(self):
        if self.pointer == len(self.cache):
            self._recv()
            if self.cache == '':
                raise self.OutputPipeError('No characters more.')
        self.pointer += 1
        return self.cache[self.pointer - 1]

    def recvline(self):
        res = ''
        while True:
            c = self.recv()
            if c != '\n':
                res += c
            else:
                break
        return res

    def recvchar(self):
        while True:
            c = self.recv()
            if c != ' ' and c != '\n' and c != '\t' and c != '\r':
                return c

    def recvint(self):
        res = 0
        while True:
            c = self.recv()
            if 48 <= ord(c) and ord(c) <= 57:
                res = res * 10 + int(c)
            else:
                break
        return res

    def __init__(self, pipe):
        assert pipe.readable()
        self.pipe = pipe
        self._reset_cache()
        # print('output', dir(pipe))


class Config:
    def __init__(self):
        self.problem_name = 'noname'
        self.sandbox_path = path.abspath(
            path.join(path.dirname(__file__), 'sandbox.py'))
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
    ps = subprocess.Popen(
        ['python', config.sandbox_path, config.solution_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    task.stdin = InputPipe(ps.stdin)
    task.stdout = OutputPipe(ps.stdout)
    try:
        judger(task)
        ps.wait()
        res = dict(status='SystemError',
                   message='[testlib] judge.py didn\'t have response.')
    except BaseResult as response:
        res = dict(status=type(response).__name__, message=str(response))
    return res


def run(tasks=None):
    if tasks is None:
        tasks = range(0, len(judgers))
    res = []
    for task in tasks:
        try:
            data = run_task(judgers[task], task_id=task)
            res.append(data)
        except BaseException as e:
            res.append(dict(status='SystemError', message=str(repr(e))))
    print('[SUCCESS]', json.dumps(res))
