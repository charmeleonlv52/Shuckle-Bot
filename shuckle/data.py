import aiohttp
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
        return f.read()

class TempDownload(object):
    '''
    A class used to download a file on entering
    a with and then deletes it on exit.
    '''
    def __init__(self, url):
        self.url = url
        now = time.time()
        _, ext = os.path.splitext(url)
        self.path = '/tmp/{}.{}'.format(self.now, ext)

    def __enter__(self):
        with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                dl = await resp.read()

                with FileLock(self.path) as f:
                    f.write(dl)

                return self.path

    def __exit__(self):
        try:
            os.remove(self.path)
        except:
            pass
