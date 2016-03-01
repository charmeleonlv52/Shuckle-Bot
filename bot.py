from config import BOTS_FOLDER, COMMANDS, DESCRIPTION, PERMISSIONS
from discord import Client
import humanfriendly
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

class Toolbox(Client):
    bot_list = []

    def __init__(self):
        super().__init__()

        self.start_time = time()
        self.__DEBUG__ = __DEBUG__

        try:
            self._load_bots()
        except:
            print('Error: Invalid bot found in bots folder')
            traceback.print_exc()
            sys.exit(0)

        print('Bots Done Loading...')

    def _load_bots(self):
        bots = os.listdir(__BOTS__)

        for bot in bots:
            # Only try importing files
            if os.path.isfile(os.path.join(__BOTS__, bot)):
                # Remove trailing .py
                bot = bot[:-3]
                # from bots.x import bot as bot
                bot = __import__('bots.{}'.format(bot), globals(), locals(), ['bot']).bot
                # Instantiate a new instance of the bot and add to list
                bot = bot(self)
                self.bot_list.append(bot)

    async def help(self, message):
        if any(message.content.startswith(x) for x in ['help', 'about', 'info']):
            if any(message.content == x for x in ['help', 'about', 'info']):
                await self.send_message(
                    message.channel,
                    DESCRIPTION.format(
                        bot_name=self.user.name,
                        uptime=humanfriendly.format_timespan(time() - self.start_time, detailed=False)
                    )
                )
            elif message.content.endswith('commands'):
                await self.send_message(
                    message.channel,
                    COMMANDS.format(bot_name=self.user.name)
                )
            elif message.content.endswith('permissions'):
                await self.send_message(
                    message.channel,
                    PERMISSIONS
                )

    async def on_message(self, message):
        mention = any([m == client.user for m in message.mentions])

        if mention or message.content.startswith('~'):
            if mention:
                # Remove initial "@bot_name "
                message.content = message.clean_content.replace('@{} '.format(self.user.name), '', 1)
            else:
                message.content = message.clean_content.replace('~', '', 1)

            await self.help(message)

            for bot in self.bot_list:
                if hasattr(bot, 'on_message'):
                    await bot.on_message(message)

client = Toolbox()

print('Starting up...')
print('Debug Status: {}'.format(__DEBUG__))
print('Using user: ' + secrets.email)

client.run(secrets.email, secrets.password)