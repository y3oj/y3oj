#-*- coding: utf-8 -*-
# require Python version >= 3.8

from os import path


def get_arg(index):
    from sys import argv
    if index >= len(argv) or argv[index] == 'inherit':
        return None
    return argv[index]


def get_path(basepath):
    return path.join(path.abspath(path.dirname(__file__)), basepath)


def register_audithook():
    from sys import addaudithook

    def block_mischief(event, arg):
        if type(event) != str:
            raise TypeError('[sandbox] Type of `event` should be `str`.')
        if event == 'open' and type(arg[1]) == str and arg[1] != 'r':
            print('\taudit:', event, arg)
            raise IOError('file write forbidden')
        if event.split('.')[0] in ['subprocess', 'shutil', 'winreg']:
            print('\taudit:', event, arg)
            raise IOError(
                'potentially dangerous, filesystem-accessing functions forbidden'
            )

    addaudithook(block_mischief)
    del (block_mischief)


code_path = get_path(get_arg(1) or 'sol.py')
with open(code_path, 'r+', encoding='utf-8') as file:
    code = file.read()

allow_objects = {'SANDBOX_ON': True}

exec(code, allow_objects)
