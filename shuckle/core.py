from config import BOTS_FOLDER, COMMANDS, DESCRIPTION, PERMISSIONS
from discord import Client
import humanfriendly
import os
from secrets import secrets
import sys
from time import time
import traceback
from util import get_internal

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

                prefix, cmd = method._shuckle_command

                if prefix not in self.prefixes:
                    self.prefixes[prefix] = {}

                # Check for namespace collisions
                if cmd in self.prefixes[prefix]:
                    print('Error: Found duplicate definition for <{} {}>'.format(prefix, cmd))
                    sys.exit(0)

                self.prefixes[prefix][cmd] = method

    def run(self, email, password):
        try:
            self._load_bots()
        except:
            print('Error: Invalid bot found in bots folder')
            traceback.print_exc()
            sys.exit(0)

        print('Bots Done Loading...')

        self.client.run(email, password)

    def get_channel(self):
        return get_internal('_channel')

    async def say(self, message, *args, **kwargs):
        await self.client.send_message(self.get_channel(), message, *args, **kwargs)

    async def upload(self, f, *args, **kwargs):
        await self.client.send_file(self.get_channel(), f, *args, **kwargs)

    async def delete(self, message):
        await self.client.delete_message(message)

    def get_history(self, **kwargs):
        return self.client.logs_from(self.get_channel(), **kwargs)

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

            print(message.content)

            await self.help(message)

            try:
                prefix = message.content.split(' ')[0]
                command = message.content.split(' ')[1]
                message.content = ' '.join(message.content.split(' ')[2:])

                if prefix in self.prefixes:
                    method = self.prefixes[prefix][command]
                    await method(message)
            except IndexError:
                pass
            except:
                traceback.print_exc()