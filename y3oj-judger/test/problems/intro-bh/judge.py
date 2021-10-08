# -*- coding: UTF-8 -*-

import testlib
from testlib import Random, Accepted, WrongAnswer

n = None
m = None
luck = []


def before_judge(task):
    global n, m, luck
    gen = Random(str(task.id) + task.testlib.problem_name)

    # n
    n = gen.randint(50, 100)

    # m
    if task.id == 0:
        m = 1
    elif task.id == 3:
        m = n
    else:
        m = gen.randint(n // 4, n // 4 * 3)

    # luck
    while True:
        luck = ['chepaihao%06d' % gen.randint(1, 999999) for _ in range(n)]
        if len(luck) == len(set(luck)):  # 说明 luck 数组无重复元素
            break

    # file io
    with open('bh.csv', 'w+', encoding='utf-8') as file:
        file.write('\n'.join(luck))


def judge(task):
    assert n is not None and m is not None and len(luck) != 0

    task.recvthis('请输入要抽取的车牌数: ')
    task.sendline(m)

    rsp = [task.recvline() for _ in range(m)]

    if len(rsp) != len(set(rsp)):
        raise WrongAnswer('输出中有重复元素。')

    for line in rsp:
        if line not in luck:
            raise WrongAnswer(f'`{line}` 不在待选车牌中。')

    raise Accepted('恭喜你通过了这个数据点！')


testlib.config.problem_name = 'intro-bh'
testlib.register(judge, range(4))
testlib.register(before_judge, range(4), type='before')
testlib.run()
