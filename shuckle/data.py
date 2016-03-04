from fcntl import lockf, LOCK_EX, LOCK_UN
import os

def write_binary(path, data):
    try:
        with open(path, 'wb+') as f:
            lockf(f, LOCK_EX)
            f.write(data)
            lockf(f, LOCK_UN)

        return True
    except:
        return False

def read_binary(path):
    data = None

    try:
        with open(path, 'rb') as f:
            lockf(f, LOCK_EX)
            data = f.read()
            lockf(f, LOCK_UN)
    except:
        pass
    finally:
        return data

def write_file(path, data):
    try:
        with open(path, 'w+') as f:
            lockf(f, LOCK_EX)
            f.write(data)
            lockf(f, LOCK_UN)

        return True
    except:
        return False

def read_file(path):
    data = None

    try:
        with open(path, 'w+') as f:
            lockf(f, LOCK_EX)
            data = f.read()
            lockf(f, LOCK_UN)
    except:
        pass
    finally:
        return data
