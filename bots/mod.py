import asyncio
from datetime import datetime
import os
from shuckle.command import command
import time

# Arbitrarily large number that we
# will hopefully never reach.
MAX_INT = 99999999999999999999
# 15 megabytes
MAX_ATTACHMENT = 15 * 1024 * 1024

HELP = """
__Mod Commands:__

Deletes all messages in a channel (potentially slow) [B:MM/B:H/U:MM/U:H]:
```
@{bot_name} mod clear
```
Saves all previous messages in a text file and sends it to the user (15 MB max archive size; potentially slow) [B:MM/B:H/U:MM/U:H]
```
@{bot_name} mod archive
```
Prunes all messages by a user [B:MM/U:MM]:
```
@{bot_name} mod prune <@user>
```
"""

class ModBot(object):
    __group__ = 'mod'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self, message):
        await self.client.say(HELP.strip().format(bot_name=self.client.user.name))

    @command(perm=['manage_messages'])
    async def clear(self, message):
        await self.prune_channel(message)

    @command(perm=['manage_messages'])
    async def prune(self, message):
        mentions = message.mentions

        await self.prune_channel(
            message,
            func=lambda x: x.author in mentions
        )

    # Deletes all previous messages in a specified
    # channel given a message. Does not delete the
    # given message.
    async def prune_channel(self, message, func=None):
        history = self.client.get_history(limit=MAX_INT)

        async for x in history:
            if func is not None and func(x) or func is None:
                await self.client.delete(x)

    # Archives an entire channel to a text file
    # and sends it to the calling user.
    @command('archive', perm=['manage_messages', 'read_message_history'])
    async def archive_channel(self, message):
        history = self.client.get_history(limit=MAX_INT)
        now = datetime.utcnow().strftime('%m-%d-%y-%H%M%S')
        path = os.path.join('/tmp', '{}.txt'.format(time.time()))

        size = 0

        with open(path, 'w+') as f:
            async for x in history:
                out = '[{}] {}: {}\n'.format(x.timestamp, x.author.name, x.clean_content)

                if size + len(out) > MAX_ATTACHMENT:
                    break

                f.write(out)
            f.flush()

        channel = str(message.channel).replace(' ', '-')
        server = str(message.server).replace(' ', '-')

        with open(path, 'rb') as f:
            filename = '{}.{}-{}.txt'.format(server, channel, now)
            content = 'Here is the archive you requested:'

            await self.client.attach(message.author, f, content=content, filename=filename)

        os.remove(path)

bot = ModBot
