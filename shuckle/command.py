import json

'''
Shuckle commands are space delimited.
'''

'''
Parses a string as a command.

Returns:
    - group
    - cmd
    - args
'''
def parse_cmd(content):
    tokens = content.split(' ')
    group = tokens[0]

    try:
        cmd = tokens[1]
    except:
        cmd = None

    try:
        args = ' '.join(tokens[2:])
    except:
        args = None

    return group, cmd, args

class Command(object):
    def __init__(self, cmd, func, perm=[]):
        self.cmd = cmd
        self.func = func
        self.user_perm = perm

    async def run(self, message):
        await self.func(message)

    def __repr__(self):
        return json.dumps({
            'cmd': self.cmd,
            'user_perm': self.user_perm
        })

def command(cmd=None, owner=False, perm=[]):
    def dec(func):
        if cmd is None:
            command = func.__name__
        else:
            command = cmd

        func._shuckle_command = Command(command, func, perm)
        return func
    return dec
