import aiohttp
import asyncio
import json
import pickle

from shuckle.command import command
from shuckle.data import FileLock

class Stream(object):
    def __init__(self, user, sub=False):
        self.user = user
        self.sub = sub

class TwitchBot(object):
    __group__ = 'twitch'
    __disabled__ = True

    def __init__(self, client):
        self.client = client
        self.to_check = {}

    async def setup(self):
        '''
        for each stream to check:
            if streaming:
                alert all channels for current stream
                delete channels that are not subs

        requeue async loop
        '''
        print('Setting up Twitch bot event loop...')
        return True

    @command(perm=['manage_messages'])
    def announce(self, message):
        pass

    @command(perm=['manage_messages'])
    def subscribe(self, message):
        pass

    @command()
    def notify(self, message):
        pass

bot = TwitchBot
