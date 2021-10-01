import yaml
import requests
from argparse import ArgumentParser
from os import path, popen, system as exec

from y3oj import config
from y3oj.utils import installPackage, readFile, makedirs

thirdparty_host = config.frontend.thirdparty_host


def logger(*args):
    print('[y3oj-build-frontend]', *args)


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


def build(source_dir, target_dir, forced=False):
    source_dir = path.abspath(source_dir)
    target_dir = path.abspath(target_dir)
    temp_dir = path.join(dirname, 'tmp', 'build-frontend')
    makedirs(temp_dir)
    makedirs(target_dir)

    packages = yaml.load(readFile(path.join(source_dir, 'package.yml')),
                         Loader=yaml.FullLoader)
    for name, desc in packages.items():
        logger(f'installing package {name}...')
        if path.exists(path.join(target_dir, 'lib', name)) and not forced:
            logger(f'package {name} has been installed, skipped.')
            continue
        installPackage(name, thirdparty_host, path.join(target_dir, 'lib'),
                       temp_dir, **desc)
        logger(f'installed package {name}.')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='The frontend builder for y3oj project.')
    parser.add_argument('-f', '--force')

    dirname = path.dirname(path.abspath(__file__))
    checkRequirement()
    build(path.join(dirname, 'y3oj-frontend'),
          path.join(dirname, 'y3oj', 'static'))
