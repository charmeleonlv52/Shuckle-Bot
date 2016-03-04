from .command import parse_cmd

class Frame(object):
    '''
    A class that represents the state of a command
    at its time of invocation.

    Properties:
        message: The message used to construct the Frame
        author: The author of the message
        channel: The channel of invocation
        server: The server of invocation
        mentions: A list of mentions in the message without
                  the calling mention (if applicable)
        group: The command group
        cmd: The command itself
        args: All command arguments as they appear in the message
    '''
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
