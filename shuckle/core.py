from config import BOTS_FOLDER, COMMANDS, DESCRIPTION, PERMISSIONS
from discord import Client
import humanfriendly
import os
from secrets import secrets
import sys
from time import time
import traceback
from util import get_internal

class ShuckleError(Error):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'Shuckle Error: {}'.format(self.message)

class ShucklePermissionError(ShuckleError):
    def __init__(self):
        super().__init__('Insufficient permission to perform this operation.')


class Toolbox(object):
    def __init__(self, base, bots, debug):
        self.start_time = time()

        self.__DEBUG__ = debug
        self.__BASE__ = base
        self.__BOTS__ = bots

        self.prefixes = {}
        self.client = Client()
        self.user = None

        setattr(self.client, 'on_message', self.on_message)    

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

            # Register it in the command list
            for method_name in dir(bot):
                method = getattr(bot, method_name)

                # Has this method been flagged for registration?
                if not hasattr(method, '_shuckle_command'):
                    continue

                command = method._shuckle_command
                prefix = command.prefix
                cmd = command.command

                if prefix not in self.prefixes:
                    self.prefixes[prefix] = {}

                # Check for namespace collisions
                if cmd in self.prefixes[prefix]:
                    raise ShuckleError('Error: Found duplicate definition for <{} {}>'.format(prefix, cmd))

                self.prefixes[prefix][cmd] = method

    def run(self, email, password):
        try:
            self._load_bots()
        except:
            if self.__DEBUG__: traceback.print_exc()
            raise ShuckleError('Error: Invalid bot found in bots folder')

        print('Bots done loading...')
        print('Shuckle is ready...')

        self.client.run(email, password)

    @property
    def channel(self):
        return get_internal('_channel')

    async def say(self, message, *args, **kwargs):
        await self.client.send_message(self.self.channel, message, *args, **kwargs)

    async def upload(self, f, *args, **kwargs):
        await self.client.send_file(self.self.channel, f, *args, **kwargs)

    async def delete(self, message):
        await self.client.delete_message(message)

    def get_history(self, **kwargs):
        return self.client.logs_from(self.self.channel, **kwargs)

    async def help(self, message):
        if any(message.content.startswith(x) for x in ['help', 'about', 'info']):
            if any(message.content == x for x in ['help', 'about', 'info']):
                await self.say(
                    DESCRIPTION.format(
                        bot_name=self.user,
                        uptime=humanfriendly.format_timespan(time() - self.start_time, detailed=False)
                    )
                )
            elif message.content.endswith('commands'):
                await self.say(
                    message.channel,
                    COMMANDS.format(bot_name=self.user.name)
                )
            elif message.content.endswith('permissions'):
                await self.say(
                    message.channel,
                    PERMISSIONS
                )

    def has_perm(self, user, perm_list):
        perm = self.channel.permissions_for(user)
        return all(getattr(perm, x, False) for x in perm_list)

    async def on_message(self, message):
        if message.author == self.user:
            return

        mention = any([m == self.client.user for m in message.mentions])

        if mention or message.content.startswith('~'):
            _channel = message.channel

            if self.user is None:
                self.user = self.client.user.name

            if mention:
                # Remove initial "@bot_name "
                message.content = message.clean_content.replace('@{} '.format(self.user), '', 1)
            else:
                message.content = message.clean_content.replace('~', '', 1)

            await self.help(message)

            try:
                prefix = message.content.split(' ')[0]
                command = message.content.split(' ')[1]
                message.content = ' '.join(message.content.split(' ')[2:])

                if prefix in self.prefixes:
                    method = self.prefixes[prefix][command]

                    if not self.has_perm(message.author, method.user_perm):
                        self.say('You don\'t have permission to use this command. :(')
                    if not self.has_perm(self.user, method.bot_perm):
                        raise ShucklePermissionError()

                    await method(message)
            except IndexError:
                pass
            except ShuckleError e:
                self.say(e)
            except:
                traceback.print_exc()