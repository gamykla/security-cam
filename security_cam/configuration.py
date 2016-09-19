import os


class Configuration(object):

    def get_value(self, key):
        return os.environ.get(key)
