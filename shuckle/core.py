import asyncio
from discord import Client, errors, Member
import humanfriendly
import inspect
import os
import sys
from time import time
import traceback

from config import config
from secrets import secrets

from .db.module import is_enabled
from .error import *
from .frame import Frame
from .tokenizer import Tokenizer
from .transform import transform_bool, transform_timespan
from .types import Module, Timespan
from .util import get_id, get_internal

class Toolbox(object):
    def __init__(self, debug=False):
        self.start_time = time()

        self.__DEBUG__ = debug

        self.commands = {}
        self.setup = []
        self.teardown = []
        self.client = Client()
        self.user = None

        self.core = {
            'help': self.help,
            'info': self.help,
            'about': self.help,
            'invite': self.invite
        }

        self.client.on_ready = self.on_ready
        self.client.on_message = self.on_message

        self.delete = self.client.delete_message
        self.attach = self.client.send_file

    def _try_load(self, bot):
        '''
        Attempt to load a single bot given
        an instance of it.
        '''
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
                    raise ShuckleError('Found duplicate definition for <{}.{}>'.format(x, cmd))

                command.func = method
                self.commands[x][cmd] = command

        # If the bot has a setup add it to setup list
        if hasattr(bot, 'setup') and hasattr(bot.setup, '__call__'):
            self.setup.append(bot)
        if hasattr(bot, 'teardown') and hasattr(bot.teardown, '__call__'):
            self.teardown.append(bot)

    def _load_bots(self):
        '''
        Attempt to load all bots in the bots folder.
        '''
        bots = os.listdir(config.__BOTS__)

        for bot in bots:
            # Only try importing files
            if not os.path.isfile(os.path.join(config.__BOTS__, bot)):
                continue

            # Remove trailing .py
            bot = bot[:-3]
            # from bots.x import bot as bot
            bot = __import__('bots.{}'.format(bot), globals(), locals(), ['bot']).bot
            # Instantiate a new instance of the bot and add to list
            bot = bot(self)
            # Try loading the bot
            self._try_load(bot)

    def _unload_bots(self):
        '''
        Teardown and unload all bots.
        '''
        for bot in self.teardown:
            bot.teardown()

        self.commands = {}

    def run(self, token):
        try:
            self._load_bots()
        except:
            if self.__DEBUG__: traceback.print_exc()
            raise ShuckleError('Invalid bot found in bots folder')

        print('Bots done loading...')

        if self.__DEBUG__: print(self.commands)

        print('Shuckle is starting...')

        self.client.run(token)

    def remove_prefix(self, message):
        '''
        Attempts to remove the calling prefix from a message.
        Returns True if it was removed (Shuckle was called).
        Returns False if it was not (Shuckle was not called).
        '''
        mention = message.content.startswith(self.user.mention)
        prefix = message.content.startswith(config.prefix)

        if mention or prefix:
            if mention:
                message.content = message.content.replace(self.user.mention, '', 1)
            else:
                message.content = message.content.replace(config.prefix, '', 1)

            return True
        return False

    def _gen_args(self, frame, tokens, func):
        '''
        Attempts to match tokens to function
        parameters. Parameters with no annotation
        should only be used as the last one as they are
        passed any remaining tokens as a list.
        '''
        signature = inspect.signature(func)
        args = []

        try:
            for param in signature.parameters:
                param = signature.parameters[param]
                annotation = param.annotation

                if annotation is int:
                    args.append(int(tokens.next()))
                elif annotation is bool:
                    args.append(transform_bool(tokens.next()))
                elif annotation is str:
                    args.append(tokens.next())
                elif annotation is Member:
                    user_id = get_id(tokens.next())
                    args.append(frame.server.get_member(user_id))
                elif annotation is Timespan:
                    args.append(transform_timespan(tokens.next()))
                elif annotation is Module:
                    test = tokens.peek().lower()
                    if test in self.commands:
                        args.append(test)
                        tokens.next()
                    else:
                        raise
                elif annotation is Frame:
                    args.append(frame)
                else:
                    args.append(tokens.swallow())
        except ValueError:
            args.append(tokens.swallow())
        except:
            # Typically we will want to swallow
            # _gen_arg errors because it means an invalid
            # command was issued.
            if self.__DEBUG__: traceback.print_exc()
            raise ShuckleArgumentError()

        return args

    async def exec_command(self, frame):
        '''
        Attempt to execute a command given
        its invocation frame.
        '''
        # Internal variables are set here because
        # asyncio loops run separate to our stack.
        #
        # This means get_internal will not find
        # these variables if we declare and define them
        # in on_message.
        _channel = frame.channel
        _author = frame.author

        tokens = Tokenizer(frame.message)

        try:
            group = tokens.next()
        except:
            group = tokens.swallow()

        try:
            cmd = tokens.next()
        except:
            cmd = tokens.swallow()

        # Module not enabled for given channel.
        if not is_enabled(frame.channel.id, group):
            return

        try:
            try:
                # There is a limited number of commands
                # belonging to no group. All of them are core
                # commands. In this case the group
                # is the command.
                if cmd is None:
                    func = self.core[group]
                elif group in self.commands:
                    command = self.commands[group][cmd]

                    if not self.has_perm(frame.author, command.user_perm):
                        raise ShuckleUserPermissionError()
                    if command.owner and frame.author.id != config.owner_id:
                        raise ShuckleUserPermissionError()

                    func = command.func
                else:
                    return

                args = self._gen_args(frame, tokens, func)

                try:
                    await func(*args)
                except errors.Forbidden:
                    raise ShucklePermissionError()
            except IndexError:
                pass
            except KeyError:
                pass
            except TypeError:
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

        for bot in self.setup:
            await bot.setup()

        print('Shuckle is ready...')

    # on_message event handler
    async def on_message(self, message):
        if self.user is None:
            return
        if message.author == self.user:
            return

        if self.remove_prefix(message):
            await self.exec_command(Frame(message))

    ##################################
    # WRAPPER FUNCTIONS
    ##################################

    async def say(self, message, channel=None, *args, **kwargs):
        if channel is None:
            channel = get_internal('_channel')

        await self.client.send_message(channel, message, *args, **kwargs)

    async def tell(self, *args, **kwargs):
        await self.say(*args, channel=get_internal('_author'), **kwargs)

    async def upload(self, f, *args, **kwargs):
        await self.client.send_file(get_internal('_channel'), f, *args, **kwargs)

    def get_history(self, **kwargs):
        return self.client.logs_from(get_internal('_channel'), **kwargs)

    async def purge_from(self, *args, **kwargs):
        await self.client.purge_from(*args, **kwargs)

    async def purge(self, check=lambda x: True, **kwargs):
        await self.client.purge_from(get_internal('_channel'), check=check, **kwargs)

    @property
    def author(self):
        return get_internal('_author')

    @property
    def channel(self):
        return get_internal('_channel')

    @property
    def uptime(self):
        return humanfriendly.format_timespan(time() - self.start_time, detailed=False)

    def has_perm(self, user, perm_list):
        perm = get_internal('_channel').permissions_for(user)
        return all(getattr(perm, x, False) for x in perm_list)

    ##################################
    # CORE COMMANDS
    ##################################

    async def invite(self):
        await self.tell('Authorize me at the following URL: https://discordapp.com/oauth2/authorize?&client_id=173665672629452800&scope=bot&permissions=0')

    async def help(self):
        '''
        Display general information about Shuckle:
        @{bot_name} help|about|info
        '''
        await self.say(
            config.description.format(
                bot_name=self.user.name,
                uptime=self.uptime,
                bot_list=', '.join(sorted(self.commands.keys())),
                prefix=config.prefix
            )
        )
