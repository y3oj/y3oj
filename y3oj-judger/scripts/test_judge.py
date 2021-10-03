import testlib
from os import path
from sys import stderr
from testlib import Random


def judge(task):
    def logger(*args):
        stderr.write(' '.join(map(str, ['[judge{}]'.format(task.id), *args])) +
                     '\n')

    logger('start')
    logger(task)
    gen = Random(str(task.id) + task.testlib.problem_name)
    a = gen.randint(1, 100)
    b = gen.randint(1, 100)
    logger('send', a, b)
    task.send('{} {}'.format(a, b))
    c = task.recv_int()
    logger('recv', c)

    if a + b == c:
        return dict(status='Accepted')
    else:
        return dict(status='Wrong Answer',
                    message='{} plus {} should be {}.'.format(a, b, c))


testlib.config.problem_name = 'a_plus_b'
testlib.config.solution_path = path.abspath(
    path.join(path.dirname(__file__), 'test_sol.py'))
testlib.register_judger(judge, range(3))
testlib.run()
