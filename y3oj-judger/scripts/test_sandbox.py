import random
from os import path


def test_globals():
    assert 'SANDBOX_ON' in globals()


def test_read_file():
    dir = path.abspath(path.dirname(__file__))
    with open(path.join(dir, 'sandbox.py'), 'r', encoding='utf-8') as file:
        code = file.read()
    print(code.replace('\n', '\\n')[:200])


def test_read_file_outside_workdir():
    dir = path.abspath(path.dirname(__file__))
    with open(path.abspath(path.join(dir, '..', '..', 'config.yml')),
              'r',
              encoding='utf-8') as file:
        code = file.read()
    print(code.replace('\n', '\\n')[:200])


def test_write_file():
    dir = path.abspath(path.dirname(__file__))
    with open(path.join(dir, '..', 'hack.txt'), 'w+',
              encoding='utf-8') as file:
        file.write('hacked.')


tasks = [
    test_globals, test_read_file, test_read_file_outside_workdir,
    test_write_file
]

print('Hello, World!', random.random())

for task in tasks:
    print('[y3oj-sandbox-test]', task)
    try:
        task()
        print('[y3oj-sandbox-test]', 'success!')
    except BaseException as e:
        print('[y3oj-sandbox-test]', 'error:', e)
