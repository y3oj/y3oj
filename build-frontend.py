import os
import yaml
import time
import stat
import shutil
import requests
from argparse import ArgumentParser
from os import path, system as exec
from colorama import Fore, Style
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from y3oj import config
from y3oj.utils import Container, installPackage, readFile, makedirs

thirdparty_host = config.frontend.thirdparty_host


def logger(*args):
    print(Fore.CYAN + Style.BRIGHT + '[y3oj-build-frontend]' + Style.RESET_ALL,
          *args, Style.RESET_ALL)


def disabledLogger(*args):
    pass


def copytree(src, dst, symlinks=False, ignore=None, forced=False):
    if not path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = path.join(src, item)
        d = path.join(dst, item)
        if symlinks and path.islink(s):
            if path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except:
                pass  # lchmod not available
        elif path.isdir(s):
            copytree(s, d, symlinks, ignore)
        elif not forced and path.exists(d):
            pass
        else:
            shutil.copy2(s, d)


def checkRequirement():
    class RequirementError(Exception):
        pass

    def checkLess():
        return exec('lessc --version') == 0

    def checkCDN():
        res = requests.get(thirdparty_host + '/TEST')
        return res.text == 'y3oj/static-files-host\n'

    tasks = {
        'less': checkLess,
        'cdn': checkCDN,
    }
    for requirement, checker in tasks.items():
        logger(f'checking requirement {requirement}...')
        res = checker()
        if res:
            logger(f'requirement {requirement} is satisfied.')
        else:
            raise RequirementError(
                f'check process got failed on requirement {requirement}')


def build(source_dir, target_dir, forced=False, logger=logger):
    source_dir = path.abspath(source_dir)
    target_dir = path.abspath(target_dir)
    temp_dir = path.join(dirname, 'tmp', 'build-frontend')
    makedirs(temp_dir)
    makedirs(target_dir)

    logger('copying assets tree...')
    copytree(path.join(source_dir, 'assets'), target_dir, forced=forced)
    logger('assets tree copyed.')

    # install packages
    packages = yaml.load(readFile(path.join(source_dir, 'package.yml')),
                         Loader=yaml.FullLoader)
    for name, desc in packages.items():
        if path.exists(path.join(target_dir, 'lib', name)) and not forced:
            logger(f'package {name} has been installed, ' + Fore.GREEN +
                   'skipped' + Fore.RESET + '.')
            continue
        logger(f'installing package {name}...')
        installPackage(name, thirdparty_host, path.join(target_dir, 'lib'),
                       temp_dir, **desc)
        logger(f'installed package {name}.')

    # install less
    logger(f'building less...')
    assert exec('lessc ' + path.join(source_dir, 'style.less') + ' ' +
                path.join(target_dir, 'style.min.css')) == 0
    logger(f'less files built.')


def watch(source_dir, target_dir, forced=False, logger=logger):
    changed = False

    class MyHandler(FileSystemEventHandler):
        def on_modified(self, event):
            nonlocal changed
            changed = True
            logger('MODIFIED ' + Style.BRIGHT + event.src_path)

        def on_created(self, event):
            nonlocal changed
            changed = True
            logger('CREATED ' + Style.BRIGHT + event.src_path)

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()
    logger('watching...')

    try:
        while True:
            time.sleep(1)
            if changed:
                logger('rebuilding..')
                try:
                    build(source_dir, target_dir, forced=forced, logger=logger)
                    logger('rebuilt ' + Fore.GREEN + 'successed')
                except AssertionError:
                    logger('rebuilt ' + Fore.RED + 'failed' + Fore.RESET +
                           ': AssertionError')
                changed = False
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    parser = ArgumentParser(
        description='The frontend builder for y3oj project.')
    parser.add_argument('-f', '--force', nargs='?', const=True)
    parser.add_argument('--watch', nargs='?', const=True)
    args_source = parser.parse_args().__dict__
    args = Container({
        'force': ('force' in args_source and args_source['force']) or False,
        'watch': ('watch' in args_source and args_source['watch']) or False,
    })
    logger('args', args)

    dirname = path.dirname(path.abspath(__file__))
    checkRequirement()

    source_dir = path.join(dirname, 'y3oj-frontend')
    target_dir = path.join(dirname, 'y3oj', 'static')
    build(source_dir, target_dir, forced=args.force)
    if args.watch:
        watch(source_dir, target_dir, forced=args.force)
