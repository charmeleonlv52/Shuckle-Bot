import asyncio
import humanfriendly
import json
import traceback

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

        return zip(self.options, results)

    def get_top(self):
        results = self.get_results()
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
                poll_msg = '**POLL: {}** - {}'.format(
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

                poll_msg = '**POLL: {}** - Results'.format(data['title'])

                for x in range(len(top)):
                    poll_msg += '\n{}. {} ({})'.format(x + 1, top[x][0], top[x][1])

                await self.client.send_message(message.channel, poll_msg)

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