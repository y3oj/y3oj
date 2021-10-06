import yaml
import json
from os import path

from y3oj import logger
from y3oj.utils import Container, dirname


class Config(Container):
    def merge(self, another):
        data = self.__dict__
        for key, value in another.__dict__.items():
            if key in data and \
                    isinstance(data[key], Config) and \
                    isinstance(value, Config):
                data[key] = data[key].merge(value)
            else:
                data[key] = value
        return Config(data)

    def __str__(self):
        return json.dumps({ \
                key: str(value) \
                for key, value in self.__dict__.items() \
            }).replace('\\"', '"').replace('\\\\', '\\')

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
logger.info(config, module='config')