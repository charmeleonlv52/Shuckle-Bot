import aiohttp
import asyncio
import traceback

from shuckle.command import command
from shuckle.db.twitch import  add_stream, delete_stream, get_streams, get_stream
from shuckle.error import ShuckleError
from shuckle.frame import Frame
from shuckle.util import gen_help

TWITCH_STREAM = 'https://api.twitch.tv/kraken/streams/{}'
CHECK_DELAY = 60 # 60 seconds not a config option because some people aren't the smartest

class Stream(object):
    def __init__(self, streamer, frame):
        self.channel = frame.channel
        self.streamer = streamer
        self.frame = frame

class TwitchBot(object):
    '''
    **Twitch Bot**
    Provides commands for notifying when a Twitch streamer is online.
    '''
    __group__ = 'twitch'
    headers = {
        'content-type': 'application/json'
    }

    def __init__(self, client):
        self.client = client
        self.to_check = {}
        self.loaded = False

    async def setup(self):
        streams = get_streams()
        streams = [x.frame for x in streams]

        for stream in streams:
            await self.client.exec_command(stream)

        self.loaded = True

    @command()
    async def help(self):
        '''
        Show twitch commands:
        ```
        @{bot_name} twitch help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command(perm=['manage_channels'])
    async def announce(self, frame: Frame, streamer):
        '''
        Announce, in the current channel, when somebody is streaming [U:MC]:
        ```
        @{bot_name} twitch announce <name>
        ```
        '''
        streamer = ' '.join(streamer)
        if self.loaded:
            if get_stream(frame.channel.id, streamer):
                raise ShuckleError('This streamer is already being watched.')

            stream = Stream(streamer, frame)

            if not add_stream(stream):
                raise ShuckleError('Unable to add stream to watch list.')

            await self.client.say('Okay. I will make a one-time announcement when **{}** starts streaming.'.format(streamer))

        route = TWITCH_STREAM.format(streamer)

        async def do_task():
            while True:
                try:
                    with aiohttp.ClientSession() as session:
                        async with session.get(route, headers=self.headers) as resp:
                            if resp.status == 200:
                                body = await resp.json()

                                if body['stream'] is not None:
                                    await self.client.say('**{}** is now streaming!'.format(streamer))
                                    delete_stream(frame.channel.id, streamer)
                                    break

                    await asyncio.sleep(CHECK_DELAY)
                except:
                    traceback.print_exc()

        loop = asyncio.get_event_loop()
        asyncio.ensure_future(do_task())

bot = TwitchBot
