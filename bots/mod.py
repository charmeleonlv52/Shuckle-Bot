from datetime import datetime
from discord import errors
from shuckle.command import command

# Arbitrarily large number that we
# will hopefully never reach.
MAX_INT = 99999999999999999999

class ModBot(object):
    def __init__(self, client):
        self.client = client

    @command('mod', 'clear', perm=['manage_messages'])
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
    @command('mod', 'archive', perm=['manage_messages', 'read_message_history'])
    async def archive_channel(self, message):
        history = self.client.get_history(limit=MAX_INT, before=message)
        now = datetime.utcnow()
        path = '/tmp/{}.txt'.format(now)

        with open(path, 'w+') as f:
            async for x in history:
                f.write(str(x) + '\n')

            f.flush()

            await self.client.upload(message.author, f, filename='{} {}'.format(message.channel, now))

        os.remove(path)


bot = ModBot