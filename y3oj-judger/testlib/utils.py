import random


class Random:
    def _randint(self, a, b):
        return random.randint(a, b)

    def _randrange(self, a, b, c=None):
        if c is None:
            return random.randrange(a, b)
        else:
            return random.randrange(a, b, c)

    def __getattr__(self, name):
        if ('_' + name) in dir(self):

            def decorator(*args, **kwargs):
                current = random.getstate()
                random.setstate(self.state)
                res = getattr(self, '_' + name)(*args, **kwargs)
                self.state = random.getstate()
                random.setstate(current)
                return res

            return decorator

        else:
            raise KeyError()

    def __init__(self, seed=None):
        current = random.getstate()
        random.seed(seed, version=2)
        self.state = random.getstate()
        random.setstate(current)