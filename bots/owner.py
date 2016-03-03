from config import OWNER_ID
import os
from shuckle.command import command
from shuckle.error import ShuckleUserPermissionError
import sys

class OwnerBot(object):
    __group__ = 'owner'

    def __init__(self, client):
        self.client = client

    @command()
    async def restart(self, message):
        if message.author.id == OWNER_ID:
            os.execv(os.path.join(self.client.__BASE__, 'shuckle.py'), sys.argv)
        else:
            raise ShuckleUserPermissionError()

    @command()
    async def reload(self, message):
        if message.author.id == OWNER_ID:
            try:
                self.client._load_bots()
            except:
                pass
        else:
            raise ShuckleUserPermissionError()

bot = OwnerBot
