class Command(object):
    def __init__(self, cmd, func, perm=[], user_perm=[], bot_perm=[]):
        self.cmd = cmd
        self.func = func
        self.user_perm = user_perm
        self.bot_perm = bot_perm

        for x in perm:
            self.user_perm.append(x)
            self.bot_perm.append(x)

    async def run(self, message):
        await self.func(message)

def command(cmd=None, perm=[], user_perm=[], bot_perm=[]):
    if cmd is not None and hasattr(cmd, '__call__'):
        command = cmd.__name__
        cmd._shuckle_command = Command(command, cmd, perm, user_perm, bot_perm)

        return cmd

    def dec(func):
        if cmd is None:
            command = func.__name__
        else:
            command = cmd

        func._shuckle_command = Command(command, func, perm, user_perm, bot_perm)
        return func
    return dec