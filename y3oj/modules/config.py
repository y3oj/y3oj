import yaml
from os import path

from y3oj.utils import Container, dirname


class ConfigNode(Container):
    def merge(self, another):
        data = {}
        data.update(self.__dict__)
        data.update(another.__dict__)
        return ConfigNode(data)

    def __setitem__(self, name, val):
        if isinstance(val, dict):
            val = ConfigNode(val)
        return self.__dict__.__setitem__(name, val)

    def __init__(self, data):
        for key, value in data.items():
            self.__setitem__(key, value)


def loadConfig(dir=None):
    if dir is None:
        dir = path.abspath(path.join(dirname, '../config.yml'))
    with open(dir, 'r+', encoding='utf8') as file:
        config = file.read()
    data = yaml.load(config, Loader=yaml.FullLoader)
    return ConfigNode(data)


config = loadConfig(path.join(dirname, 'config.sample.yml')).merge(
    loadConfig(path.join(dirname, 'config.yml')))
