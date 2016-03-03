import asyncio
from datetime import datetime
import os
from shuckle.command import command
import time
from shuckle.util import gen_help

# Arbitrarily large number that we
# will hopefully never reach.
MAX_INT = 99999999999999999999
# 15 megabytes
MAX_ATTACHMENT = 15 * 1024 * 1024

class ModBot(object):
    '''
    **Mod Bot**
    Provides commands for easier channel management.
    '''
    __group__ = 'mod'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self, frame):
        '''
        Show mod commands:
        ```
        @{bot_name} mod help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command(perm=['manage_messages'])
    async def clear(self, frame):
        '''
        Deletes all messages in a channel (potentially slow) [B:MM/B:H/U:MM/U:H]:
        ```
        @{bot_name} mod clear
        ```
        '''
        await self.prune_channel()

    @command(perm=['manage_messages'])
    async def prune(self, frame):
        '''
        Prunes all messages by a user [B:MM/U:MM]:
        ```
        @{bot_name} mod prune <@user>
        ```
        '''
        mentions = frame.mentions

        await self.prune_channel(
            func=lambda x: x.author in mentions
        )

    # Deletes all previous messages in a specified
    # channel.
    async def prune_channel(self, func=None):
        history = self.client.get_history(limit=MAX_INT)

        async for x in history:
            if func is None or func(x):
                await self.client.delete(x)

    # Archives an entire channel to a text file
    # and sends it to the calling user.
    @command('archive', perm=['manage_messages', 'read_message_history'])
    async def archive_channel(self, frame):
        '''
        Saves all previous messages in a text file and sends it to the user (15 MB max archive size; potentially slow) [B:MM/B:H/U:MM/U:H]:
        ```
        @{bot_name} mod archive
        ```
        '''
        history = self.client.get_history(limit=MAX_INT)
        now = datetime.utcnow().strftime('%m-%d-%y-%H%M%S')
        path = os.path.join('/tmp', '{}.txt'.format(time.time()))

        with open(path, 'wb+') as f:
            async for x in history:
                out = '[{}] {}: {}\n'.format(x.timestamp, x.author.name, x.clean_content)
                out = out.encode('utf-8')

                f.write(out)

                if f.tell() > MAX_ATTACHMENT:
                    f.truncate(MAX_ATTACHMENT)
                    break

            f.flush()

            channel = str(frake.channel).replace(' ', '-')
            server = str(frame.server).replace(' ', '-')

            filename = '{}.{}-{}.txt'.format(server, channel, now)
            content = 'Here is the archive you requested:'

            await self.client.attach(frame.author, f, content=content, filename=filename)

        os.remove(path)

bot = ModBot
