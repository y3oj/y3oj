import sys
from colorama import Fore, Style


class Logger:
    class SubLogger:
        def info(self, *args):
            self.logger.info(*args, module=self.prefix)

        def warn(self, *args):
            self.logger.warn(*args, module=self.prefix)

        def error(self, *args):
            self.logger.error(*args, module=self.prefix)

        def __init__(self, logger, prefix):
            self.logger = logger
            self.prefix = prefix

    def printer(self, *args, **kwargs):
        level = kwargs['level']
        prefix = self.level_color[level] + '[' + level + ']'
        if 'module' in kwargs:
            prefix += Fore.CYAN + Style.BRIGHT + '[' + kwargs['module'] + ']'
        prefix += ' ' + Style.RESET_ALL
        sys.stderr.write(prefix + ' '.join(map(str, args)) + '\n')

    def module(self, name):
        return self.SubLogger(self, name)

    def info(self, *args, **kwargs):
        self.printer(*args, **kwargs, level='INFO')

    def warn(self, *args, **kwargs):
        self.printer(*args, **kwargs, level='WARN')

    def error(self, *args, **kwargs):
        self.printer(*args, **kwargs, level='ERROR')

    def __init__(self, name):
        self.name = name
        self.level_color = {
            'INFO': Fore.GREEN + Style.BRIGHT,
            'WARN': Fore.YELLOW + Style.BRIGHT,
            'ERROR': Fore.RED + Style.BRIGHT,
        }


logger = Logger('y3oj')
logger.info('hello', 'world')
