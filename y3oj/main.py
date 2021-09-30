import yaml
from os import path
from flask import Flask

from y3oj.utils import Container


class ConfigNode(Container):
    def __setitem__(self, name, val):
        if isinstance(val, dict):
            val = ConfigNode(val)
        return self.__dict__.__setitem__(name, val)

    def __init__(self, data):
        for key, value in data.items():
            self.__setitem__(key, value)


def loadConfig(dir=None):
    if dir is None:
        current = path.dirname(path.abspath(__file__))
        dir = path.abspath(path.join(current, '../config.yml'))
    with open(dir, 'r+', encoding='utf8') as file:
        config = file.read()
    data = yaml.load(config, Loader=yaml.FullLoader)
    return ConfigNode(data)


app = Flask(__name__)
config = loadConfig()