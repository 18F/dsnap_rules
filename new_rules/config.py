from collections import namedtuple


Config = namedtuple('Config', ['allows_working'])


def get_config():
    return Config(allows_working=True)
