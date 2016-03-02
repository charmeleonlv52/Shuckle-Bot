from config import STATS_DETAIL
from humanfriendly import format_size
from psutil import virtual_memory
from shuckle.command import command

class StatBot(object):
    __group__ = ['stats']

    def __init__(self, client):
        self.client = client

    @command
    async def show(self, message):
        used_mem = virtual_memory().used
        total_mem = virtual_memory().total

        await self.client.say(
            STATS_DETAIL.format(
                uptime=self.client.uptime,
                used_mem=format_size(used_mem),
                total_mem=format_size(total_mem),
                server_count=self.client.server_count
            )
        )

bot = StatBot