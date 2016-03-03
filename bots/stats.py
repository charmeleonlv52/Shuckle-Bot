from humanfriendly import format_size
from psutil import virtual_memory
from shuckle.command import command
from shuckle.util import gen_help

class StatBot(object):
    '''
    **Stat Bot**
    Provides commands to show various statistics.
    '''
    __group__ = 'stats'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self, message):
        '''
        Show stat commands:
        ```
        @{bot_name} stats help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command()
    async def show(self, message):
        '''
        Show Shuckle statistics:
        ```
        @{bot_name} stats show
        ```
        '''
        used_mem = virtual_memory().used
        total_mem = virtual_memory().total

        await self.client.say(
            STATS_DETAIL.strip().format(
                uptime=self.client.uptime,
                used_mem=format_size(used_mem),
                total_mem=format_size(total_mem),
                server_count=self.client.server_count
            )
        )

bot = StatBot
