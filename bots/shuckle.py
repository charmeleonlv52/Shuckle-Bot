import os
import subprocess
import sys

from config import config

from shuckle.command import command
from shuckle.error import ShuckleError
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
    async def restart(self):
        '''
        Restarts Shuckle:
        ```
        @{bot_name} shuckle restart
        ```
        '''
        await self.client.say('Restarting Shuckle...')
        os.execv(os.path.join(config.__MAIN__), sys.argv)

    @command(owner=True)
    async def update(self):
        '''
        Pulls the latest version of Shuckle from
        Github and restarts.
        ```
        @{bot_name} shuckle update
        ```
        '''

        if not subprocess.check_output('git pull', shell=True):
            raise ShuckleError('Unable to pull latest version from Github.')
        await self.restart()


bot = ShuckleBot
