class ModBot(object):
    def __init__(self, client):
        self.client = client

    # Deletes all previous messages in a specified
    # channel given a message. Does not delete the
    # given message.
    async def prune_channel(self, message, include=False):
        deleted = True

        async def delete_messages():
            async for x in self.client.logs_from(message.channel, before=message):
                deleted = True
                await self.client.delete_message(x)

        while deleted:
            deleted = False
            await delete_messages()

        if include:
            await self.client.delete_message(message)

    async def on_message(self, message):
        if message.content.startswith('mod clear'):
            if message.channel.permissions_for(message.author).manage_messages:
                await self.prune_channel(message, include=True)

bot = ModBot