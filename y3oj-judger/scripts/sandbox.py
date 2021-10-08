#-*- coding: utf-8 -*-

#############################################
#                                           #
#    **require Python version >= 3.8**      #
#  This is the sandbox for y3oj project.    #
#  I don't know if it is dangerous.         #
#  DON'T use it in product envirment.       #
#  If you have hacked this sandbox,         #
#  please submit an issue here:             #
#      https://github.com/y3oj/y3oj/issues  #
#  Thank you most sincerely.                #
#                         2021.10 @memset0  #
#                                           #
#############################################

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
        def raiseError(name):
            errors = {
                'event_type_error':
                (TypeError, 'Type of `event` should be `str`.'),
                'dangerous_syscall':
                (EnvironmentError, 'Dangerous syscall is forbidden.'),
                'opened_file_exceeded':
                (IOError, 'Too many opened file handles.'),
            }
            assert name in errors
            stderr.write('[y3oj-sandbox] audit: [{}] {}\n'.format(
                event, str(arg)))
            raise errors[name][0]('[y3oj-sandbox] ' + errors[name][1])

        file_opened_count = 0

        # stderr.write('\taudit:{} {}\n'.format(event, str(arg)))
        if type(event) != str:
            raiseError('event_type_error')
        if event.split('.')[0] in ['subprocess', 'shutil', 'winreg']:
            raiseError('dangerous_syscall')
        if event.split('.')[0] == 'os' and event.split('.')[1] not in [
                'listdir'
        ]:
            raiseError('dangerous_syscall')
        if event.split('.')[0] == 'ctypes' and event.split('.')[1] not in [
                'dlopen', 'dlsym'
        ]:
            raiseError('dangerous_syscall')
        if event == 'open':
            file_opened_count += 1
            if file_opened_count >= 1000:
                raiseError('opened_file_exceeded')

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
