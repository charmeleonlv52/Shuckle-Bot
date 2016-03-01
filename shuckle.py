from config import BOTS_FOLDER, COMMANDS, DESCRIPTION, PERMISSIONS
from discord import Client
import humanfriendly
import inspect
import os
from secrets import secrets
import sys
from time import time
import traceback

if '--debug' in sys.argv:
    __DEBUG__ = True
elif '-d' in sys.argv:
    __DEBUG__ = True
else:
    __DEBUG__ = False

__BASE__ = os.path.abspath(os.path.dirname(__file__))
__BOTS__ = os.path.join(__BASE__, BOTS_FOLDER)

# sys.path.append(__BASE__)

def _get_internal(name):
    stack = inspect.stack()

    try:
        for frame in stack:
            frame = frame[0].f_locals

            if name in frame:
                return frame[name]

        return None
    except:
        pass

class Toolbox(object):
    def __init__(self):
        self.start_time = time()
        self.__DEBUG__ = __DEBUG__

        self.bot_list = []
        self.prefixes = {}
        self.client = Client()
        self.user = None

        setattr(self.client, 'on_message', self.on_message)

    def command(self, prefix, cmd):
        def dec(func):
            func._command = (prefix, cmd)
            return func
        return dec

    def _load_bots(self):
        bots = os.listdir(__BOTS__)

        for bot in bots:
            # Only try importing files
            if not os.path.isfile(os.path.join(__BOTS__, bot)):
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

                if not hasattr(method, '_command'):
                    continue

                prefix, cmd = method._command

                if prefix not in self.prefixes:
                    self.prefixes[prefix] = {}

                self.prefixes[prefix][cmd] = method
            self.bot_list.append(bot)

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
        return _get_internal('_channel')

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
                    await method(message)
            except:
                traceback.print_exc()
                pass

client = Toolbox()
command = client.command

if __name__ == '__main__':
    print('Starting up...')
    print('Debug Status: {}'.format(__DEBUG__))
    print('Using user: ' + secrets.email)

    client.run(secrets.email, secrets.password)