from fcntl import lockf, LOCK_EX, LOCK_UN
import os

class FileLock(object):
    '''
    A class used to obtain exclusive locks
    on files to ensure atomic writes.
    '''
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
    '''
    Writes data to a file.
    '''
    with FileLock(path, mode='w') as f:
        f.write(data)

def read_file(path):
    '''
    Returns the contents of a given file.
    '''
    with open(path, 'r') as f:
        return r.read()
