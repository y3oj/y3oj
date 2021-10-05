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
    a = gen.randint(1, 10000)
    b = gen.randint(1, 10000)
    logger('send', a, b)
    task.send('{} {}'.format(a, b))
    c = task.recv_int()
    logger('recv', c)

    if a + b == c:
        return dict(status='Accepted')
    else:
        return dict(status='WrongAnswer',
                    message='{} plus {} should be {}.'.format(a, b, c))


testlib.config.problem_name = 'a_plus_b'
testlib.register_judger(judge, range(10))
testlib.run()
