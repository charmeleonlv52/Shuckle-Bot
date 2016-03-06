from config import config

from shuckle.command import command
from shuckle.error import ShuckleError
from shuckle.frame import Frame
from shuckle.module import enable_module, disable_module, is_enabled
from shuckle.types import Module
from shuckle.util import gen_help

class ModuleBot(object):
    '''
    **Module Bot**
    Provides commands for enabling and disabling individual modules.
    '''
    __group__ = 'module'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self):
        '''
        Shows module commands:
        ```
        @{bot_name} poll help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command(perm=['manage_channels'])
    async def enable(self, frame: Frame, module: Module):
        '''
        Enables a module for the current channel [U:MC]:
        ```
        @{bot_name} module enable <module>
        ```
        '''
        if enable_module(frame.channel.id, module):
            await self.client.say('The module {} has been enabled.'.format(module))
        else:
            raise ShuckleError('Unable to enable module.')

    @command(perm=['manage_channels'])
    async def disable(self, frame: Frame, module: Module):
        '''
        Disables a module for the current channel [U:MC]:
        ```
        @{bot_name} module disable <module>
        ```
        '''
        if module in config.frozen_modules:
            raise ShuckleError('You may not disable this module.')

        if disable_module(frame.channel.id, module):
            await self.client.say('The module {} has been disabled.'.format(module))
        else:
            raise ShuckleError('Unable to disable module.')

    @command(perm=['manage_channels'])
    async def toggle(self, frame: Frame, module: Module):
        '''
        Toggles a module for the current channel [U:MC]:
        ```
        @{bot_name} module toggle <module>
        ```
        '''
        if is_enabled(frame.channel.id, module):
            await self.disable(frame, module)
        else:
            await self.enable(frame, module)

bot = ModuleBot
