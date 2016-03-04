import json

'''
Shuckle commands are space delimited.
'''

class Command(object):
    '''
    A class used to represent a Shuckle command.
    '''
    def __init__(self, cmd, perm=[]):
        self.cmd = cmd
        self.user_perm = perm
        self.func = None

    def __repr__(self):
        return json.dumps({
            'cmd': self.cmd,
            'user_perm': self.user_perm
        })

def command(cmd=None, perm=[]):
    '''
    A decorator used to denote a Shuckle command.
    '''
    def dec(func):
        if cmd is None:
            command = func.__name__
        else:
            command = cmd

        func._shuckle_command = Command(command, perm)
        return func
    return dec
