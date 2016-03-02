from config import COMMANDS, PERMISSIONS
from shuckle.command import command

class GeneralBot(object):
    __group__ = ['help', 'info', 'about']

    def __init__(self, client):
        self.client = client

    @command
    async def commands(self, message):
        await self.client.say(
            COMMANDS.format(bot_name=self.client.user.name)
        )

    @command
    async def permissions(self, message):
        await self.client.say(
            PERMISSIONS
        )

bot = GeneralBot