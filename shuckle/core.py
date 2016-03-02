from config import DESCRIPTION
from discord import Client, errors
import humanfriendly
import os
from secrets import secrets
from command import Template
import sys
from time import time
import traceback
from util import get_internal

class ShuckleError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ShucklePermissionError(ShuckleError):
    def __init__(self):
        super().__init__('I don\'t have permission to do this.')

class Toolbox(object):
    def __init__(self, base, bots, prefix=None, debug=False):
        self.start_time = time()

        self.__DEBUG__ = debug
        self.__BASE__ = base
        self.__BOTS__ = bots
        self.__PREFIX__ = prefix

        self.commands = {}
        self.client = Client()
        self.user = None

        setattr(self.client, 'on_ready', self.on_ready)
        setattr(self.client, 'on_message', self.on_message)

    def _try_load(self, bot):
        if not hasattr(bot, '__group__'):
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
                    raise ShuckleError('Error: Found duplicate definition for <{} {}>'.format(x, cmd))

                command.func = method
                self.commands[x][cmd] = command

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

    @property
    def channel(self):
        return get_internal('_channel')

    @property
    def uptime(self):
        return humanfriendly.format_timespan(time() - self.start_time, detailed=False)

    @property
    def iden(self):
        return get_internal('_iden')
    

    async def say(self, message, *args, **kwargs):
        await self.client.send_message(self.channel, message, *args, **kwargs)

    async def tell(self, *args, **kwargs):
        await self.client.send_message(get_internal('_author'), *args, **kwargs)

    async def upload(self, f, *args, **kwargs):
        await self.client.send_file(self.channel, f, *args, **kwargs)

    async def delete(self, *args, **kwargs):
        await self.client.delete_message(*args, **kwargs)

    async def edit(self, *args, **kwargs):
        await self.client.edit_message(*args, **kwargs)

    def get_history(self, **kwargs):
        return self.client.logs_from(self.channel, **kwargs)

    def has_perm(self, user, perm_list):
        perm = self.channel.permissions_for(user)
        return all(getattr(perm, x, False) for x in perm_list)

    # Display Shuckle help information.
    async def help(self, message):
        if message.cmd is not None:
            return

        if any(message.group == x for x in ['help', 'about', 'info']):
            await self.say(
                DESCRIPTION.format(
                    bot_name=self.user.name,
                    uptime=self.uptime,
                    bot_list=', '.join(sorted(self.commands.keys())),
                    prefix=self.__PREFIX__
                )
            )

    # Ready event handler
    async def on_ready(self):
        self.user = self.client.user
        self.server_count = 0

        for x in self.client.servers:
            self.server_count += 1

        print('Shuckle is online...')

    # on_message event handler
    async def on_message(self, message):
        if message.author == self.user:
            return

        mention_text = '@{} '.format(self.user.name)
        mention = message.clean_content.startswith(mention_text)

        if mention or message.content.startswith(self.__PREFIX__):
            _channel = message.channel
            _author = message.author
            _iden = self.user if mention else self.__PREFIX__

            template = Template(message, mention_text if mention else self.__PREFIX__)

            await self.help(template)

            try:
                if template.group in self.commands:
                    command = self.commands[template.group][template.cmd]

                    if not self.has_perm(message.author, command.user_perm):
                        self.say('You don\'t have permission to use this command. :(')

                    try:
                        print(template.group, template.cmd)
                        await command.run(template)
                    except errors.Forbidden:
                        raise ShucklePermissionError()
            except IndexError:
                pass
            except KeyError:
                if self.__DEBUG__: traceback.print_exc()
                pass
            except ShuckleError as e:
                await self.say(e)
            except:
                traceback.print_exc()