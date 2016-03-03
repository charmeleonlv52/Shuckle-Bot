from config import PERMISSIONS
from shuckle.command import command

class GeneralBot(object):
    __group__ = ['help', 'info', 'about']
    __disabled__ = False

    def __init__(self, client):
        self.client = client

    @command()
    async def permissions(self, message):
        await self.client.say(
            PERMISSIONS
        )

bot = GeneralBot
