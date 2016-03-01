from datetime import datetime
from discord import errors
import os
from shuckle.command import command
import time

# Arbitrarily large number that we
# will hopefully never reach.
MAX_INT = 99999999999999999999
# 15 megabytes
MAX_ATTACHMENT = 15 * 1024 * 1024

class ModBot(object):
    __group__ = 'mod'

    def __init__(self, client):
        self.client = client

    @command('clear', perm=['manage_messages'])
    async def clear(self, message):
        await self.prune_channel(message, include=True)

    # Deletes all previous messages in a specified
    # channel given a message. Does not delete the
    # given message.
    async def prune_channel(self, message, func=None, include=False):
        history = self.client.get_history(limit=MAX_INT, before=message)

        async for x in history:
            if func is not None and func(x) or func is None:
                await self.client.delete(x)

        if include:
            await self.client.delete(message)

    # Archives an entire channel to a text file
    # and sends it to the calling user.
    @command('archive', perm=['manage_messages', 'read_message_history'])
    async def archive_channel(self, message):
        history = self.client.get_history(limit=MAX_INT, before=message)
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
            await self.client.client.send_file(message.author, f, filename='{}.{}-{}.txt'.format(server, channel, now))

        os.remove(path)


bot = ModBot