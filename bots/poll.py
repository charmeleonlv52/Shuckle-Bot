import asyncio
from humanfriendly import format_timespan
import json
import os
import pygal
from pygal.style import Style
import time
import traceback

from shuckle.command import command
from shuckle.error import ShuckleError
from shuckle.frame import Frame
from shuckle.types import Timespan
from shuckle.util import gen_help

DiscordStyle = Style(
    background='#ffffff',
    plot_background='#ffffff',
    font_family='Open Sans',
    foreground='#546e7a',
    foreground_strong='#546e7a',
    foreground_subtle='#546e7a',
    colors=('#738bd7', '#1abc9c', '#3498db', '#e91e63', '#f1c40f')
)

def make_chart(title, values):
    chart = pygal.Pie(
        title=title,
        legend_at_bottom=True,
        style=DiscordStyle
    )

    for value in values:
        chart.add('{} ({})'.format(value[0], value[1]), value[1])

    now = time.time()
    path = os.path.join('/tmp', '{}.png'.format(now))

    chart.render_to_png(path)

    return path

class Poll(object):
    def __init__(self, title, options):
        self.title = title
        self.votes = {}
        self.options = options
        self.closed = False

    def vote(self, option, uid):
        if option <= 0 or option > len(self.options):
            return

        self.votes[uid] = option

    def get_results(self):
        results = [0 for x in self.options]

        for x in self.votes:
            results[self.votes[x] - 1] += 1

        if sum(results) == 0:
            return None

        return zip(self.options, results)

    def get_top(self):
        results = self.get_results()

        if results is None:
            return None

        return sorted(results, key=lambda x: x[1], reverse=True)

class PollBot(object):
    '''
    **Poll Bot**
    Provides commands for poll creation.
    '''
    __group__ = 'poll'
    polls = {}

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self):
        '''
        Shows poll commands:
        ```
        @{bot_name} poll help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command()
    async def start(self, frame: Frame, title: str, duration: Timespan, options):
        '''
        Create a new poll in the current channel (does not support user mentions) [B:AF]:
        ```
        @{bot_name} poll start {{
            "title": <string>,
            "duration": <integer|seconds>,
            "options": [<string>] // Note: This is an array of strings not an indicator for optional.
        }}
        ```
        Shorthand for the above [B:AF]:
        ```
        @{bot_name} poll start <title> <duration> <option> [<option>]
        ```
        '''
        # Only one poll per channel
        if frame.channel in self.polls:
            raise ShuckleError('This channel already has a poll in progress.')
        try:
            try:
                data = json.loads(title)
                title = data['title']
                duration = data['duration']
                options = data['options']
            except:
                # Shorthand
                if self.client.__DEBUG__ and duration > 5 * 60:
                    return

            poll = Poll(title, options)
            self.polls[frame.channel] = poll

            # Create poll message and send it
            poll_msg = '**POLL: {}** - Ends in {}'.format(title, format_timespan(duration))

            for x in range(len(options)):
                poll_msg += '\n{}. {}'.format(x + 1, options[x])

            await self.client.say(poll_msg)

            # Sleep for some time
            await asyncio.sleep(duration)

            if poll.closed:
                return

            # Get top options and send a message
            top = poll.get_top()

            if top is not None:
                chart = make_chart(title, top)

                # Upload chart.
                with open(chart, 'rb') as f:
                    await self.client.upload(f)

                try:
                    os.remove(chart)
                except:
                    pass
            else:
                await self.client.say('**POLL: {}** - No Results'.format(data['title']))

            # Delete current poll to allow a new one
            del self.polls[frame.channel]
        except:
            traceback.print_exc()

    @command()
    async def vote(self, frame: Frame, option : int):
        '''
        Cast your vote for the current poll:
        ```
        @{bot_name} poll vote <integer>
        ```
        '''
        # Check to see if there's even a poll to vote on
        if not frame.channel in self.polls:
            return
        self.polls[frame.channel].vote(option, frame.author.id)

    @command(perm=['manage_messages'])
    async def stop(self, frame: Frame):
        '''
        Delete the current poll and don't show the results [U:MM]:
        ```
        @{bot_name} poll stop
        ```
        '''
        try:
            self.polls[frame.channel].closed = True
            del self.polls[frame.channel]
        except:
            raise ShuckleError('This channel does not have a poll in progress.')

bot = PollBot
