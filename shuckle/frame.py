class Frame(object):
    '''
    A class that represents the state of a command
    at its time of invocation.

    Properties:
        message: The message content without the calling prefix
        server: The server of invocation
        channel: The channel of invocation
        author: The author of the message
    '''
    def __init__(self, message, parent=None):
        self.server = message.server
        self.channel = message.channel
        self.author = message.author
        self.message = message.content
        self.parent = parent
