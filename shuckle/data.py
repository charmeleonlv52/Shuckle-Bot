from fcntl import lockf, LOCK_EX, LOCK_UN
import os

class FileLock(object):
    def __enter__(path, mode='wb+'):
        self.f = open(path, mode)

        lockf(self.f, LOCK_EX)
        return f

    def __exit__(*args, **kwargs):
        lockf(self.f, LOCK_UN)
        self.f.flush()
        self.f.close()

def write_file(path, data):
    with FileLock(path, mode='w+') as f:
        f.write(data)

def read_file(path):
    with FileLock(path, mode='r') as f:
        return f.read()
