import asyncio
import humanfriendly
import json
import os
import pygal
from pygal.style import Style
import time
import traceback

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
    path = '/tmp/{}.png'.format(now)

    chart.render_to_png(path)

    return path

class Poll(object):
    def __init__(self, title, options):
        self.title = title
        self.votes = {}
        self.options = options
        self.closed = False

    def vote(self, option, uid):
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
    polls = {}

    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        MAKE_POLL = 'poll make '
        DELETE_POLL = 'poll delete'
        VOTE = 'poll vote '

        if message.content.startswith(MAKE_POLL):
            # Only one poll per channel
            if message.channel in self.polls:
                return
            try:
                # Parse string starting from MAKE_POLL
                data = ''.join(message.content.split(MAKE_POLL)[1:])
                
                try:
                    data = json.loads(data)
                except:
                    # Shorthand
                    try:
                        data = data.split(':')

                        try:
                            duration = int(humanfriendly.parse_timespan(data[1]))
                        except:
                            duration = int(data[1])

                        if self.client.__DEBUG__ and duration > 5 * 60:
                            return

                        data = {
                            'title': data[0],
                            'duration': duration,
                            'options': data[2:]
                        }
                    except:
                        return

                poll = Poll(data['title'], data['options'])
                self.polls[message.channel] = poll

                # Create poll message and send it
                poll_msg = '**POLL: {}** - Ends in {}'.format(
                    data['title'],
                    humanfriendly.format_timespan(data['duration'])
                )

                for x in range(len(data['options'])):
                    poll_msg += '\n{}. {}'.format(x + 1, data['options'][x])

                await self.client.send_message(message.channel, poll_msg)

                # Sleep for some time
                await asyncio.sleep(data['duration'])

                if poll.closed:
                    return

                # Get top options and send a message
                top = self.polls[message.channel].get_top()

                if top is not None:
                    chart = make_chart(data['title'], top)

                    # Upload chart.
                    with open(chart, 'rb') as f:
                        await self.client.send_file(message.channel, f)

                        try:
                            os.remove(chart)
                        except:
                            pass
                else:
                    await self.client.send_message(message.channel, '**POLL: {}** - No Results'.format(data['title']))

                '''
                poll_msg = '**POLL: {}** - Results'.format(data['title'])

                for x in range(len(top)):
                    poll_msg += '\n{}. {} ({})'.format(x + 1, top[x][0], top[x][1])

                await self.client.send_message(message.channel, poll_msg)
                '''

                # Delete current poll to allow a new one
                del self.polls[message.channel]
            except:
                traceback.print_exc()
        elif message.content.startswith(VOTE):
            # Check to see if there's even a poll to vote on
            if not message.channel in self.polls:
                return
            try:
                # Get vote option
                option = int(message.content.split(VOTE)[1])
                self.polls[message.channel].vote(option, message.author.id)
            except:
                traceback.print_exc()
        elif message.content.startswith(DELETE_POLL):
            if message.channel.permissions_for(message.author).manage_messages:
                try:
                    self.polls[message.channel].closed = True
                    del self.polls[message.channel]
                except:
                    pass

bot = PollBot