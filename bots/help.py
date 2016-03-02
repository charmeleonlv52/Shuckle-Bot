from config import MOD, PERMISSIONS, POLL
from shuckle.command import command

class GeneralBot(object):
    __group__ = ['help', 'info', 'about']

    def __init__(self, client):
        self.client = client

    @command
    async def poll(self, message):
        await self.client.say(
            POLL.format(bot_name=self.client.user.name)
        )

    @command
    async def mod(self, message):
        await self.client.say(
            MOD.format(bot_name=self.client.user.name)
        )

    @command
    async def permissions(self, message):
        await self.client.say(
            PERMISSIONS
        )

bot = GeneralBot