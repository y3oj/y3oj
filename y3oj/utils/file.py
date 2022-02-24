import os
from os import path

dirname = path.abspath(path.join(path.dirname(path.abspath(__file__)), '..', '..'))


def path_join(*args):
    return os.path.abspath(os.path.join(*args))


def makedirs(dir):
    if path.exists(dir):
        return
    os.makedirs(dir)


def readFile(dir):
    makedirs(path.dirname(dir))
    with open(dir, 'r+', encoding='utf8') as file:
        return file.read()


def writeFile(dir, content):
    makedirs(path.dirname(dir))
    with open(dir, 'w+', encoding='utf8') as file:
        return file.write(content)


def readBinaryFile(dir):
    makedirs(path.dirname(dir))
    with open(dir, 'rb+') as file:
        return file.read()


def writeBinaryFile(dir, content):
    makedirs(path.dirname(dir))
    with open(dir, 'wb+') as file:
        return file.write(content)


def listDir(dir):
    dir = path.abspath(dir)
    return map(lambda basename: path.join(dir, basename), os.listdir(dir))


def download(url, dir, **args):
    from requests import get
    res = get(url, **args)
    writeBinaryFile(dir, res.content)


def unzip(source_file, target_dir):
    from zipfile import ZipFile
    with ZipFile(source_file, 'r') as zipped_file:
        zipped_file.extractall(target_dir)


def basename(dir):
    return path.splitext(path.basename(dir))[0]