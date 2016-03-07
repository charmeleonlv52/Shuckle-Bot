import aiohttp
import asyncio

from shuckle.command import command
from shuckle.db.twitch import  add_stream, get_streams, get_stream
from shuckle.frame import Frame
from shuckle.error import ShuckleError

TWITCH_STREAM = 'https://api.twitch.tv/kraken/streams/{}'
CHECK_DELAY = 60 # 60 seconds not a config option because some people aren't the smartest

class Stream(object):
    def __init__(self, streamer, frame):
        self.channel = frame.channel
        self.streamer = streamer
        self.frame = frame

class TwitchBot(object):
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

            await self.client.say('Okay. I will make a one-time announcement when {} starts streaming.'.format(streamer))

        route = TWITCH_STREAM.format(streamer)

        while True:
            with aiohttp.ClientSession() as session:
                async with session.get(route, headers=self.headers) as resp:
                    if resp.status == 200:
                        body = await resp.json()

                        if body['stream'] is not None:
                            await self.client.say('{} is now streaming!'.format(stream))
                            delete_stream(frame.channel.id, streamer)
                            break

            await asyncio.sleep(CHECK_DELAY)

bot = TwitchBot
