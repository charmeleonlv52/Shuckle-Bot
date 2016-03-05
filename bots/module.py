from shuckle.command import command
from shuckle.error import ShuckleError
from shuckle import module
from shuckle.types import Module

class ModuleBot(object):
    def __init__(self, client):
        self.client = client

    @command(perm=['manage_channels'])
    async def enable(self, frame: frame, module: Module):
        if module.enable(frame.channel.id, module):
            await self.client.say('The module {} has been enabled.'.format(module))
        else:
            raise ShuckleError('Unable to enable module.')

    @command(perm=['manage_channels'])
    async def disable(self, module: Module):
        if module.disable_module(module):
            await self.client.say('The module {} has been disabled.'.format(module))
        else:
            raise ShuckleError('Unable to disable module.')

bot = ModuleBot
