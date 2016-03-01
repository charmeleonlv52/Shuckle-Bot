class Command(object):
	def __init__(prefix, cmd, perm=[], user_perm=[], bot_perm=[]):
		self.prefix = prefix
		self.cmd = cmd
		self.user_perm = user_perm
		self.bot_perm = bot_perm

		for x in perm:
			self.user_perm.append(x)
			self.bot_perm.append(x)

def command(prefix, cmd, perm=[], user_perm=[], bot_perm=[]):
    def dec(func):
        func._shuckle_command = Command(prefix, cmd, perm, user_perm, bot_perm)
        return func
    return dec