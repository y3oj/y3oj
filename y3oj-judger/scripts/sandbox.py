#-*- coding: utf-8 -*-
'''
**require Python version >= 3.8**
This is the sandbox for y3oj project.
I don't know if it is dangerous,
so DON'T use it in product envirment.
If you can hack this sandbox,
please submit an issue here:
    https://github.com/y3oj/y3oj/issues
Thank you most sincerely.
                       2021.10 @memset0
'''

from os import path
from sys import stderr


def get_arg(index):
    from sys import argv
    if index >= len(argv) or argv[index] == 'inherit':
        return None
    return argv[index]


def get_path(basepath):
    return path.join(path.abspath(path.dirname(__file__)), basepath)


def register_audithook():
    from os import path
    from sys import addaudithook

    def block_mischief(event, arg):
        if type(event) != str:
            raise TypeError('[sandbox] Type of `event` should be `str`.')
        if event == 'open' and arg[1] != 'r':
            stderr.write('\taudit:{} {}\n'.format(event, str(arg)))
            raise IOError('[sandbox] File write operation is forbidden.')
        if event.split('.')[0] in ['subprocess', 'shutil', 'winreg']:
            stderr.write('\taudit:{} {}\n'.format(event, str(arg)))
            raise IOError('[sandbox] Dangerous syscall is forbidden.')
        if event == 'open':
            realpath = path.abspath(arg[0])
            workdir = path.abspath(path.dirname(__file__))
            if '__pycache__' in realpath or \
                realpath.endswith('.py') or \
                realpath.endswith('.pyc') or \
                path.dirname(realpath).startswith(workdir):
                return
            stderr.write('\taudit:{} {}\n'.format(event, str(arg)))
            raise IOError('[sandbox] File read outside workdir is forbidden.')

    addaudithook(block_mischief)
    del (block_mischief)


code_path = get_path(get_arg(1) or 'sol.py')
try:
    with open(code_path, 'r', encoding='utf-8') as file:
        code = file.read()
except:
    code = ''

register_audithook()
exec(code, dict(SANDBOX_ON=True, __file__=code_path))
