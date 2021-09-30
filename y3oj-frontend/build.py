from os import path, popen


def build(target_dir):
    print('咕咕咕')
    raise Exception('在路上了')


if __name__ == '__main__':
    dirname = path.dirname(path.abspath(__file__))
    build(path.join(dirname, '..', 'static'))