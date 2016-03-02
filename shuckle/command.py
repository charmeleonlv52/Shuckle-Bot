import json

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

class Template(object):
    def __init__(self, message, iden):
        content = message.clean_content.replace(iden, '', 1)
        tokens = content.split(' ')

        self.raw_message = message
        self.author = message.author
        self.channel = message.channel
        self.server = message.server

        self.group, self.cmd, self.args = parse_cmd(content)

def command(cmd=None, perm=[]):
    if cmd is not None and hasattr(cmd, '__call__'):
        command = cmd.__name__
        cmd._shuckle_command = Command(command, cmd, perm)

        return cmd

    def dec(func):
        if cmd is None:
            command = func.__name__
        else:
            command = cmd

        func._shuckle_command = Command(command, func, perm)
        return func
    return dec