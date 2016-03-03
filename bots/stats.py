from humanfriendly import format_size
from psutil import virtual_memory
from shuckle.command import command
from shuckle.util import gen_help

HELP = """
__Stats Commands:__
Show stats for geeks:
```
@{bot_name} stats show
```
"""

STATS_DETAIL = """
__Stats for Geeks:__
Uptime: {uptime}
Total Memory: {total_mem}
Used Memory: {used_mem}
Connected Servers: {server_count}
"""

class StatBot(object):
    __group__ = 'stats'

    def __init__(self, client):
        self.client = client

    @command()
    async def help(self, message):
        await self.client.say(HELP.strip().format(bot_name=self.client.user.name))

    @command()
    async def show(self, message):
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
