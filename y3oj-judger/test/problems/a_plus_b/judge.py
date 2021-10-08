import testlib
from sys import stderr
from testlib import Random, Accetped, WrongAnswer


def judge(task):
    gen = Random(str(task.id) + task.testlib.problem_name)
    a = gen.randint(1, 10000)
    b = gen.randint(1, 10000)
    task.sendline('{} {}'.format(a, b))
    c = task.recvint()

    if a + b == c:
        raise Accetped
    else:
        raise WrongAnswer(f'{a} plus {b} shout be {a + b}, but got {c}.')


testlib.config.problem_name = 'a_plus_b'
testlib.register_judger(judge, range(10))
testlib.run()
