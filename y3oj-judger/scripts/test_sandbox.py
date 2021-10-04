import random
from os import path
from colorama import Fore, Style


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


def test_os_system():
    import os
    os.system('echo hacked.')


def test_os_popen():
    from os import popen
    popen('echo hacked.')


tasks = [
    test_globals, test_read_file, test_read_file_outside_workdir,
    test_write_file, test_os_system, test_os_popen
]

print('Hello, World!', random.random())

for task in tasks:
    prefix = Fore.CYAN + Style.BRIGHT + '[y3oj-sandbox-test]' + Style.RESET_ALL
    print(prefix, str(task))
    try:
        task()
        print(prefix, Fore.GREEN + 'success!' + Style.RESET_ALL)
    except BaseException as e:
        print(prefix, Fore.RED + 'error' + Style.RESET_ALL + ':', e)
