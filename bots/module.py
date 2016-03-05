from shuckle.command import command
from shuckle.types import Module

class ModuleBot(object):
    def __init__(self, client):
        self.client = client

    @command(perm=['manage_channels'])
    async def enable(self, module: Module):
        self.client.enable_module(module)
        await self.client.say('The module {} has been enabled.'.format(module))

    @command(perm=['manage_channels'])
    async def disable(self, module: Module):
        self.client.disable_module(module)
        await self.client.say('The module {} has been disabled.'.format(module))

bot = ModuleBot
