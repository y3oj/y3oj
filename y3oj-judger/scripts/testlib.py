import json
import random
import subprocess
from os import path

pipe_encoding = 'utf-8'


class BaseResult(Exception):
    pass


class Accepted(BaseResult):
    pass


class WrongAnswer(BaseResult):
    pass


class RuntimeError(BaseResult):
    pass


class SystemError(BaseResult):
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
        self._send(str(text) + end)

    def __init__(self, pipe):
        assert pipe.writable()
        self.pipe = pipe
        # print('input', dir(pipe))


class OutputPipe(object):
    def _reset_cache(self):
        self.cache = ''
        self.pointer = 0

    def _recv(self):
        self.cache = self.pipe.read1().decode(pipe_encoding)
        self.pointer = 0
        # print('[recv]', str(list(self.cache)))

    def recv(self):
        if self.pointer == len(self.cache):
            self._recv()
            if self.cache == '':
                raise WrongAnswer('[testlib-pipe] No characters more.')
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
        if res.endswith('\r'):
            res = res[:-1]
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

    def recvthis(self, target):
        for s in target:
            c = self.recv()
            if c != s:
                raise WrongAnswer(f'[testlib-pipe] Except {s}, recived {c}.')

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
        self.id = int(task_id)
        self.testlib = testlib_config
        self.stdin = None
        self.stdout = None


config = Config()
judgers = []


def register(judger, tasks=[], type='default'):
    assert type == 'default' or type == 'before' or type == 'after'
    for task in tasks:
        while len(judgers) <= task:
            judgers.append({})
        judgers[task][type] = judger


def run_task(judger, task_id):
    res = None
    task = Task(task_id=task_id, testlib_config=config)
    try:
        if 'before' in judger:
            judger['before'](task)
        ps = subprocess.Popen(
            ['python', config.sandbox_path, config.solution_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        task.stdin = InputPipe(ps.stdin)
        task.stdout = OutputPipe(ps.stdout)
        temperror = None
        if 'default' in judger:
            try:
                judger['default'](task)
            except BaseResult as error:
                temperror = error
        returncode = ps.wait()
        if returncode != 0:
            errlogs = ps.stderr.read1().decode(pipe_encoding).split('\n')
            lastline = None
            for i in range(len(errlogs) - 1, -1, -1):
                if errlogs[i] != '':
                    lastline = errlogs[i]
                    break
            if lastline.endswith('\r'):
                lastline = lastline[:-1]
            if lastline is None:
                raise RuntimeError()
            else:
                raise RuntimeError(lastline)
        else:
            if temperror is not None:
                raise temperror
        if 'after' in judger:
            judger['after'](task)
        raise SystemError('[testlib] judge.py didn\'t give a response.')
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
