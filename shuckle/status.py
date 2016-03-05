import json

from .data import read_file, write_file

class Status(object):
    '''
    Keeps track of whether or not a module is
    enabled given a channel ID.
    '''
    def __init__(self, modules):
        self.tracked = {x: {} for x in modules}
        self.path = None

    def load(self, path):
        self.path = path

        try:
            self.tracked = json.loads(read_file(path))
        except IOError:
            self.save_status()

    def save_status(self):
        if self.path is None:
            raise IOError('Status data file not set.')

        write_file(self.path, json.dumps(self.tracked))

    def is_enabled(self, module, channel):
        return channel not in self.tracked[module] or self.tracked[module][channel]

    def enable(self, module, channel):
        self.tracked[module][channel] = True
        self.save_status()

    def disable(self, module, channel):
        self.tracked[module][channel] = False
        self.save_status()
