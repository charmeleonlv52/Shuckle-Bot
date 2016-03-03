from command import parse_cmd

class Frame(object):
    def __init__(self, message, iden):
        self.iden = iden

        if hasattr(iden, 'name'):
            iden = '@{} '.format(iden.name)

        content = message.clean_content.replace(iden, '', 1)
        tokens = content.split(' ')

        self.message = message
        self.author = message.author
        self.channel = message.channel
        self.server = message.server
        self.mentions = message.mentions

        if iden not in content and hasattr(self.iden, 'name'):
            self.mentions.remove(self.iden)

        self.group, self.cmd, self.args = parse_cmd(content)

'''
__doc__ for command documentation
move secrets path to config
objectify config
clean up command parsing
'''
