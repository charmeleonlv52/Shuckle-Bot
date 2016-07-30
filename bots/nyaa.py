import aiohttp
import asyncio
import feedparser
import re
import traceback

from config import config

from shuckle.command import command
from shuckle.error import ShuckleError
from shuckle.frame import Frame
from shuckle.db.nyaa import get_feed, get_feeds
from shuckle.types import Module
from shuckle.util import gen_help

RELEASE_REGEX = r'\[(.+)\][ _]+(.+?)[ _]*-?[ _]*(\d+)[ _]*((\[|\().*((480|720|1080|BD)p?).*(\]|\)))?([ _]*\[.+][ _]*)?\.(\w+)'

class NyaaBot(object):
    '''
    **Nyaa Bot**
    Provides commands for subscription to Nyaa RSS feeds. This only works for releases by sub groups that follow standard convention. Filters work though.
    '''
    __group__ = 'nyaa'

    def __init__(self, client):
        self.client = client
        self.loaded = False

    async def setup(self):
        feeds = get_feeds()

        for feed in feeds:
            await self.watch(feed.channel, feed.url)

        self.loaded = True

    def watch(self, channel, rss_url, json_filter):
        async def load_rss():
            with aiohttp.ClientSession() as session:
                async with session.get(route, headers=self.headers) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    else:
                        return ''

        def pass_filter(subber, title, episode, quality, fmt):
            l = locals()
            return all(l[x] == details[x] for x in details.keys())

        async def do_task():
            while True:
                try:
                    body = get_releases()
                    feed = feedparser.parse(body)

                    for entry in feed['entries']:
                        name = entry['title']
                        details = re.search(RELEASE_REGEX, name)

                        try:
                            if details and len(details.groups) == 10:
                                subber = details.group(1)
                                title = details.group(2)
                                episode = str(int(details.group(3)))
                                quality = details.group(7)
                                fmt = details.group(10).upper()

                                if pass_filter(subber, title, episode, quality, fmt):
                                    url = entry['links'][0]['href']

                                    self.client.say(
                                        '{subber} has released episode {episode} of {title} in {quality}.\nDownload Link: {url}'.format(
                                            **locals()
                                        ),
                                        channel=channel
                                    )
                        except:
                            traceback.print_exc()
                except:
                    traceback.print_exc()

                await asyncio.sleep(CHECK_DELAY)

        loop = asyncio.get_event_loop()
        asyncio.ensure_future(do_task())

    @command()
    async def help(self):
        '''
        Shows Nyaa commands.
        ```
        @{bot_name} nyaa help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command(perm=['manage_channels'])
    async def subscribe(self, frame: Frame, rss_url, json_filter):
        '''
        Announce, in the current channel, when a new release is announced via RSS [U:MC]:
        ```
        @{bot_name} nyaa subscribe <rss_url> <json_filter>
        ```
        '''
        channel = frame.channel.id

        if self.loaded:
            if get_feed(channel, rss_url):
                raise ShuckleError('This RSS feed is already being watched.')

            if not add_feed(channel, rss_url, json_filter):
                raise ShuckleError('Unable to add feed to watch list.')

            await self.client.say(
                'Okay. I will announce when new releases come out on this RSS feed.'.format(streamer)
            )

        await self.watch(channel, rss_url, json_filter)

bot = ModuleBot
