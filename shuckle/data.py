from fcntl import lockf, LOCK_EX, LOCK_UN
import os

class FileLock(object):
    def __init__(self, path, mode='wb'):
        self.path = path
        self.mode = mode

    def __enter__(self):
        self.f = open(self.path, self.mode)

        lockf(self.f, LOCK_EX)
        return self.f

    def __exit__(self, *args):
        lockf(self.f, LOCK_UN)
        self.f.flush()
        self.f.close()

def write_file(path, data):
    with FileLock(path, mode='w') as f:
        f.write(data)

def read_file(path):
    with FileLock(path, mode='r') as f:
        return f.read()
