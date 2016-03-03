from config import OWNER_ID
import os
from shuckle.command import command
from shuckle.error import ShuckleUserPermissionError
import sys

HELP = """
__Owner Commands:__:

Restarts Shuckle:
```
@{bot_name} owner restart
```
Reload all modules:
```
@{bot_name} owner reload
```
"""

class OwnerBot(object):
    __group__ = 'owner'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self, message):
        await self.client.say(HELP.strip().format(bot_name=self.client.user.name))

    @command()
    async def restart(self, message):
        if message.author.id == OWNER_ID:
            os.execv(os.path.join(self.client.__MAIN__), sys.argv)
        else:
            raise ShuckleUserPermissionError()

bot = OwnerBot
