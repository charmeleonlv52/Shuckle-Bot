from config import OWNER_ID
import os
from shuckle.command import command
from shuckle.util import gen_help
from shuckle.error import ShuckleUserPermissionError
import sys

class OwnerBot(object):
    '''
    **Owner Bot**
    Provides commands for Shuckle's owner.
    '''
    __group__ = 'owner'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self, message):
        '''
        Shows owner commands:
        ```
        @{bot_name} owner help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command()
    async def restart(self, message):
        '''
        Restarts Shuckle:
        ```
        @{bot_name} owner restart
        ```
        '''
        if message.author.id == OWNER_ID:
            os.execv(os.path.join(self.client.__MAIN__), sys.argv)
        else:
            raise ShuckleUserPermissionError()

bot = OwnerBot
