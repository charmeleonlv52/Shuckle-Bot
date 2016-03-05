from humanfriendly import format_size
import os
from psutil import Process, virtual_memory

from shuckle.command import command
from shuckle.util import gen_help

STATS_DETAIL = """
__Stats for Geeks:__
Uptime: {uptime}
Total Memory: {total_mem}
Used Memory: {used_mem}
Bot Memory: {py_mem}
Connected Servers: {server_count}
"""

class StatBot(object):
    '''
    **Stat Bot**
    Provides commands to show various statistics.
    '''
    __group__ = 'stats'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self):
        '''
        Show stat commands:
        ```
        @{bot_name} stats help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command()
    async def show(self):
        '''
        Show Shuckle statistics:
        ```
        @{bot_name} stats show
        ```
        '''
        process = Process(os.getpid())
        virt = virtual_memory()
        py = process.memory_info()[0]
        used_mem = virt.used
        total_mem = virt.total

        await self.client.say(
            STATS_DETAIL.strip().format(
                uptime=self.client.uptime,
                py_mem=format_size(py),
                used_mem=format_size(used_mem),
                total_mem=format_size(total_mem),
                server_count=self.client.server_count
            )
        )

bot = StatBot
