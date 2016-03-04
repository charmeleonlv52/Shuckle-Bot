import asyncio
from config import config
from discord import Client, errors
from error import ShuckleError, ShucklePermissionError, ShuckleUserPermissionError
import humanfriendly
import os
from secrets import secrets
from frame import Frame
import sys
from time import time
import traceback
from util import get_internal

class Toolbox(object):
    def __init__(self, base, main, data, bots, prefix=None, debug=False):
        self.start_time = time()

        self.__DEBUG__ = debug
        self.__BASE__ = base
        self.__MAIN__ = main
        self.__DATA__ = data
        self.__BOTS__ = bots
        self.__PREFIX__ = prefix

        self.commands = {}
        self.setup = []
        self.client = Client()
        self.user = None

        setattr(self.client, 'on_ready', self.on_ready)
        setattr(self.client, 'on_message', self.on_message)

    def _try_load(self, bot):
        if not hasattr(bot, '__group__'):
            return
        if hasattr(bot, '__disabled__') and bot.__disabled__:
            return

        prefix = bot.__group__

        # Register it in the command list
        for method_name in dir(bot):
            method = getattr(bot, method_name)

            # Has this method been flagged for registration?
            if not hasattr(method, '_shuckle_command'):
                continue

            command = method._shuckle_command
            cmd = command.cmd

            if not isinstance(prefix, list):
                prefix = [prefix]
            for x in prefix:
                if x not in self.commands:
                    self.commands[x] = {}

                # Check for namespace collisions
                if cmd in self.commands[x]:
                    raise ShuckleError('Error: Found duplicate definition for <{}.{}>'.format(x, cmd))

                command.func = method
                self.commands[x][cmd] = command

        # If the bot has a setup add it to setup list
        if hasattr(bot, 'setup') and hasattr(bot.setup, '__callable__'):
            self.setup.append(bot)

    def _load_bots(self):
        bots = os.listdir(self.__BOTS__)

        for bot in bots:
            # Only try importing files
            if not os.path.isfile(os.path.join(self.__BOTS__, bot)):
                continue

            # Remove trailing .py
            bot = bot[:-3]
            # from bots.x import bot as bot
            bot = __import__('bots.{}'.format(bot), globals(), locals(), ['bot']).bot
            # Instantiate a new instance of the bot and add to list
            bot = bot(self)
            # Try loading the bot
            self._try_load(bot)

    def run(self, email, password):
        try:
            self._load_bots()
        except:
            if self.__DEBUG__: traceback.print_exc()
            raise ShuckleError('Invalid bot found in bots folder')

        print('Bots done loading...')

        if self.__DEBUG__: print(self.commands)

        print('Shuckle is starting...')

        self.client.run(email, password)

    async def exec_command(self, frame):
        # Internal variables are set here because
        # asyncio loops run separate to our stack.
        #
        # This means get_internal will not find
        # these variables if we declare and define them
        # in on_message.
        _channel = frame.channel
        _author = frame.author
        _iden = frame.iden

        try:
            try:
                # There is a limited number of commands
                # with no group. All of them are core
                # commands.
                if frame.cmd is None:
                    await self.help(message)

                if frame.group in self.commands:
                    command = self.commands[frame.group][frame.cmd]

                    if not self.has_perm(frame.author, command.user_perm):
                        raise ShuckleUserPermissionError()
                    try:
                        await command.run(frame)
                    except errors.Forbidden:
                        raise ShucklePermissionError()
                    except Exception as e:
                        raise e
            except IndexError:
                pass
            except KeyError:
                pass
            except ShuckleError as e:
                if self.__DEBUG__: traceback.print_exc()
                await self.say(e)
            except:
                traceback.print_exc()
        except errors.Forbidden:
            print('Error: No write permission for {}.{}'.format(frame.server, frame.channel))

    # Ready event handler
    async def on_ready(self):
        self.user = self.client.user
        self.server_count = 0

        for x in self.client.servers:
            self.server_count += 1

        print('Shuckle is online...')
        print('Running bot setup functions...')
        print('Shuckle is ready...')

        for bot in self.setup:
            await bot.setup()

    # on_message event handler
    async def on_message(self, message):
        if message.author == self.user:
            return

        mention_text = '@{} '.format(self.user.name)
        mention = message.clean_content.startswith(mention_text)

        if mention or message.content.startswith(self.__PREFIX__):
            iden = self.user if mention else self.__PREFIX__
            frame = Frame(message, iden)

            # Swallow help command errors
            # they aren't important

            await self.exec_command(frame)

    ##################################
    # WRAPPER FUNCTIONS
    ##################################

    async def say(self, message, *args, **kwargs):
        await self.client.send_message(get_internal('_channel'), message, *args, **kwargs)

    async def tell(self, *args, **kwargs):
        await self.client.send_message(get_internal('_author'), *args, **kwargs)

    async def upload(self, f, *args, **kwargs):
        await self.client.send_file(self.channel, f, *args, **kwargs)

    async def delete(self, *args, **kwargs):
        await self.client.delete_message(*args, **kwargs)

    async def edit(self, *args, **kwargs):
        await self.client.edit_message(*args, **kwargs)

    async def attach(self, *args, **kwargs):
        await self.client.send_file(*args, **kwargs)

    def get_history(self, **kwargs):
        return self.client.logs_from(get_internal('_channel'), **kwargs)

    @property
    def uptime(self):
        return humanfriendly.format_timespan(time() - self.start_time, detailed=False)

    def has_perm(self, user, perm_list):
        perm = get_internal('_channel').permissions_for(user)
        return all(getattr(perm, x, False) for x in perm_list)

    ##################################
    # CORE COMMANDS
    ##################################

    async def help(self, message):
        '''
        Display general information about Shuckle:
        @{bot_name} help|about|info
        '''
        if any(message.group == x for x in ['help', 'about', 'info']):
            await self.say(
                message.channel,
                config.description.format(
                    bot_name=self.user.name,
                    uptime=self.uptime,
                    bot_list=', '.join(sorted(self.commands.keys())),
                    prefix=self.__PREFIX__
                )
            )
