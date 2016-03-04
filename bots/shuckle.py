from config import config
import os
from shuckle.command import command
from shuckle.util import gen_help
from shuckle.error import ShuckleUserPermissionError
import sys

class ShuckleBot(object):
    '''
    **Shuckle Bot**
    Provides commands for Shuckle's owner.
    '''
    __group__ = 'shuckle'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self, frame):
        '''
        Shows shuckle commands:
        ```
        @{bot_name} shuckle help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command()
    async def restart(self, frame):
        '''
        Restarts Shuckle:
        ```
        @{bot_name} shuckle restart
        ```
        '''
        if frame.author.id == config.owner_id:
            await self.client.say('Restarting Shuckle...')
            os.execv(os.path.join(self.client.__MAIN__), sys.argv)
        else:
            raise ShuckleUserPermissionError()

    @command()
    async def reload(self, frame):
        '''
        Reloads all Shuckle modules:
        ```
        @{bot_name} shuckle reload
        ```
        '''
        if frame.author.id == config.owner_id:
            self.client._unload_bots()
            self.client._load_bots()

            await self.client.say('Reloading modules...')
        else:
            raise ShuckleUserPermissionError()

bot = ShuckleBot
