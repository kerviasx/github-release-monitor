import collections
import os

class Settings(collections.defaultdict):
    def __init__(self, conf):
        super(Settings, self).__init__()
        for k in dir(conf):
            if k[0].isupper():
                v = getattr(conf, k)
                if k.endswith("_PATH"):
                    v = self.normalize_path(v)
                setattr(self, k, v)
                self[k] = v

    def __str__(self):
        ret_str = '\n[SETTINGS-START]\n'
        for k in self.keys():
            ret_str += "%s: %s\n" % (k, self[k])
        return ret_str + '[SETTINGS-END]\n'

    def __missing__(self, key):
        if key not in self.keys():
            return None
        return self[key]

    @staticmethod
    def normalize_path(path):
        return os.path.realpath(os.path.abspath(path))
