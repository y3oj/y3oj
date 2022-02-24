from os import path


class PackageError(Exception):
    pass


def installPackage(name, host, target, tempdir, type=None, version=None):
    from . import download, unzip, makedirs
    if version is None or type is None:
        raise PackageError(f'version or type of the package {name} not found')
    makedirs(path.join(target, name))
    if type == 'zip':
        download(f'{host}/{name}/{name}@{version}.zip', path.join(tempdir, name, f'{name}.zip'))
        unzip(path.join(tempdir, name, f'{name}.zip'), path.join(target, name))
