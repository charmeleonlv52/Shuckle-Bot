from discord import errors
from object import Object

# Arbitrarily large number that we
# will hopefully never reach.
MAX_INT = 99999999999999999999

class ModBot(object):
    def __init__(self, client):
        self.client = client

    # Deletes all previous messages in a specified
    # channel given a message. Does not delete the
    # given message.
    async def prune_channel(self, message, func=None, include=False):        
        async for x in self.client.logs_from(message.channel, limit=MAX_INT, before=message):
            if func is not None and func(x) or func is None:
                await self.client.delete_message(x)

        if include:
            await self.client.delete_message(message)

    async def on_message(self, message):
        if message.content.startswith('mod clear'):
            permissions_for = message.channel.permissions_for

            if permissions_for(message.author).manage_messages:
                try:
                    await self.prune_channel(message, include=True)
                except errors.Forbidden:
                    await self.client.send_message(message.channel, 'Error: Unable to prune channel--missing permissions.')

bot = ModBot