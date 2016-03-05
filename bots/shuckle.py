import os
import sys

from config import config

from shuckle.command import command
from shuckle.frame import Frame
from shuckle.util import gen_help

class ShuckleBot(object):
    '''
    **Shuckle Bot**
    Provides commands for Shuckle's owner.
    '''
    __group__ = 'shuckle'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self):
        '''
        Shows shuckle commands:
        ```
        @{bot_name} shuckle help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command(owner=True)
    async def restart(self, frame: Frame):
        '''
        Restarts Shuckle:
        ```
        @{bot_name} shuckle restart
        ```
        '''
        await self.client.say('Restarting Shuckle...')
        os.execv(os.path.join(self.client.__MAIN__), sys.argv)

bot = ShuckleBot
