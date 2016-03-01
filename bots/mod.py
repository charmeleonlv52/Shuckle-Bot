from discord import errors
from shuckle.command import command

# Arbitrarily large number that we
# will hopefully never reach.
MAX_INT = 99999999999999999999

class ModBot(object):
    def __init__(self, client):
        self.client = client

    @command('mod', 'clear')
    async def clear(self, message):
        permissions_for = message.channel.permissions_for

        if permissions_for(message.author).manage_messages:
            try:
                await self.prune_channel(message, include=True)
            except errors.Forbidden:
                await self.client.say('Error: Unable to prune channel--missing permissions.')

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

bot = ModBot