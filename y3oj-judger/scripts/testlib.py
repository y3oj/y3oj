# -*- coding: UTF-8 -*-

import sys
import json
import errno
import random
import subprocess
from os import path

pipe_encoding = 'utf-8'
warn_without_sandbox = True


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

    def _shuffle(self, a):
        return random.shuffle(a)

    def _sample(self, a, k):
        return random.sample(a, k)

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
        if config.debug:
            print('[INFO] send:', json.dumps(string))
        try:
            self.pipe.write(string.encode(pipe_encoding))
            self.pipe.flush()
        except IOError as err:
            if err.errno == errno.EPIPE:
                raise RuntimeError('[testlib] Pipe got EPIPE error, your program might run into a crash.')

    def send(self, text):
        self._send(text)

    def sendline(self, text, end='\n'):
        self._send(str(text) + end)

    def __init__(self, pipe):
        assert pipe.writable()
        self.pipe = pipe
        # print('input', dir(pipe))


class OutputPipe(object):
    EOF = -1

    def _reset_cache(self):
        self.cache = ''
        self.pointer = 0

    def _recv(self):
        self.cache = self.pipe.read1(8192).decode(pipe_encoding)
        self.pointer = 0
        if config.debug:
            print('[INFO] _recv:', json.dumps(self.cache))

    def recv(self, allow_EOF=False):
        if self.pointer == len(self.cache):
            self._recv()
            if self.cache == '':
                if allow_EOF:
                    return OutputPipe.EOF
                else:
                    raise WrongAnswer('[testlib] Read EOF from output stream.')
        self.pointer += 1
        if config.debug:
            print('[INFO] recv:', [self.cache[self.pointer - 1]])
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
        c = self.recv()
        while ord(c) < 48 or ord(c) > 57:
            c = self.recv()
        while 48 <= ord(c) and ord(c) <= 57:
            res = res * 10 + int(c)
            c = self.recv()
        return res

    def recvthis(self, target):
        for s in target:
            c = self.recv()
            if c == '\r' and s == '\n':
                c = self.recv()
            if c != s:
                raise WrongAnswer(f'[testlib] Except {s}, recived {c}.')

    def __init__(self, pipe):
        assert pipe.readable()
        self.pipe = pipe
        self._reset_cache()
        # print('output', dir(pipe))


class Config:

    def __init__(self):
        self.debug = False
        self.problem_name = 'noname'
        self.python_path = 'python'
        self.sandbox_path = path.abspath(path.join(path.dirname(__file__), 'sandbox.py'))
        self.solution_path = path.abspath(path.join(path.dirname(__file__), 'sol.py'))


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


def register(judger, tasks=None, type='default'):
    assert type == 'default' or type == 'before' or type == 'after'
    if tasks == None:
        tasks = []
    for task in tasks:
        while len(judgers) <= task:
            judgers.append({})
        judgers[task][type] = judger


def set_debug_mode(enable=True):
    config.debug = enable


def enable_debug_mode():
    set_debug_mode(enable=True)


def set_pipe_encoding(encoding):
    global pipe_encoding
    pipe_encoding = encoding


def run_task(judger, task_id):
    global warn_without_sandbox
    res = None
    if config.debug:
        print('[INFO] Task #' + str(task_id))
    task = Task(task_id=task_id, testlib_config=config)
    try:
        if 'before' in judger:
            judger['before'](task)
        if path.exists(config.sandbox_path) and not config.debug:
            parameters = [config.python_path, config.sandbox_path, config.solution_path]
        else:
            parameters = [config.python_path, config.solution_path]
            if warn_without_sandbox and not config.debug:
                print('[WARNING] `sandbox.py` not found. Don\'t use this in a production deployment.')
                warn_without_sandbox = False
        ps = subprocess.Popen(
            parameters,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        task.stdin = InputPipe(ps.stdin)
        task.stdout = OutputPipe(ps.stdout)
        temperror = None
        if 'default' in judger:
            try:
                judger['default'](task)
            except BaseResult as error:
                temperror = error
        returncode = None
        if temperror is None:
            returncode = ps.wait()
        else:
            try:
                returncode = ps.wait(timeout=0.05)
            except subprocess.TimeoutExpired:
                pass
        if config.debug:
            print('[INFO] return code = ' + str(returncode))
        if returncode is not None and returncode != 0:
            errlogs = ps.stderr.read1(8192).decode(pipe_encoding).split('\n')
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
    if config.debug:
        print('[INFO] Running in debug mode.')
    if tasks is None:
        tasks = range(0, len(judgers))
    res = []
    for task in tasks:
        try:
            data = run_task(judgers[task], task_id=task)
            res.append(data)
        except BaseException as e:
            if config.debug:
                raise e
            res.append(dict(status='SystemError', message=str(repr(e))))
    print('[SUCCESS]', json.dumps(res))
    if config.debug:
        for status in res:
            print('[STATUS]', status)
