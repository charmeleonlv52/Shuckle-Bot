import json
import os

from config import config

from .data import read_file, write_file

class Status(object):
    '''
    Keeps track of whether or not a module is
    enabled given a channel ID.
    '''
    def __init__(self, modules):
        self.tracked = {x: {} for x in modules}

    def load(self):
        path = os.path.join(config.__DATA__, 'module_status.shuckle')

        if not os.path.isfile(path):
            self.save_status()

        self.tracked = json.loads(read_file(path))

    def save_status(self):
        path = os.path.join(config.__DATA__, 'module_status.shuckle')
        write_file(path, json.dumps(self.tracked))

    def is_enabled(self, module, channel):
        return channel not in self.tracked[module] or self.tracked[module][channel]

    def enable(self, module, channel):
        self.tracked[module][channel] = True
        self.save_status()

    def disable(self, module, channel):
        self.tracked[module][channel] = False
        self.save_status()
