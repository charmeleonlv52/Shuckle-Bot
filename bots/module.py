from config import config

from shuckle.command import command
from shuckle.error import ShuckleError
from shuckle.frame import Frame
from shuckle.module import enable_module, disable_module
from shuckle.types import Module

class ModuleBot(object):
    __group__ = 'module'

    def __init__(self, client):
        self.client = client

    @command(perm=['manage_channels'])
    async def enable(self, frame: Frame, module: Module):
        if enable_module(frame.channel.id, module):
            await self.client.say('The module {} has been enabled.'.format(module))
        else:
            raise ShuckleError('Unable to enable module.')

    @command(perm=['manage_channels'])
    async def disable(self, frame: Frame, module: Module):
        if module in config.frozen_modules:
            raise ShuckleError('You may not disable this module.')
            
        if disable_module(frame.channel.id, module):
            await self.client.say('The module {} has been disabled.'.format(module))
        else:
            raise ShuckleError('Unable to disable module.')

bot = ModuleBot
