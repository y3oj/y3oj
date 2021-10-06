import yaml
from os import path

from y3oj.utils import Container, dirname


class Config(Container):
    def merge(self, another):
        data = {}
        data.update(self.__dict__)
        data.update(another.__dict__)
        return Config(data)

    def __setitem__(self, name, val):
        if isinstance(val, dict):
            val = Config(val)
        return self.__dict__.__setitem__(name, val)

    def __init__(self, data):
        for key, value in data.items():
            self.__setitem__(key, value)


def load_config(dir=None):
    if dir is None:
        dir = path.abspath(path.join(dirname, '../config.yml'))
    with open(dir, 'r+', encoding='utf8') as file:
        config = file.read()
    data = yaml.load(config, Loader=yaml.FullLoader)
    return Config(data)


config = load_config(path.join(dirname, 'config.sample.yml')).merge(
    load_config(path.join(dirname, 'config.yml')))
