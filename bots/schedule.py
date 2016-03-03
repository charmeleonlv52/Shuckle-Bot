import asyncio
import humanfriendly
from shuckle.command import command, parse_cmd

HELP = """
__Schedule Commands:__

Lists all scheduled tasks to run [U:MM]:
```
@{bot_name} schedule list
```
Adds a task to be run at a set interval [U:MM]:
```
@{bot_name} schedule add <task name> <interval> <command (no prefix)>
```
Removes as task from the scheduler [U:MM]:
```
@{bot_name} schedule delete <task name>
```
"""

class ScheduleBot(object):
    __group__ = 'schedule'

    def __init__(self, client):
        self.client = client
        self.tasks = {}

    @command()
    async def help(self, message):
        await self.client.say(HELP.strip().format(bot_name=self.client.user.name))

    @command(perm=['manage_messages'])
    async def list(self, message):
        task_list = []

        print(self.tasks)

        for task in sorted(self.tasks.keys()):
            task_list.append('{}: {}'.format(task, self.tasks[task]))

        task_list = '\n'.join(task_list)
        await self.client.say('Here is a list of scheduled tasks: \n{}'.format(task_list))

    @command(perm=['manage_messages'])
    async def delete(self, message):
        name, delay, rest = parse_cmd(message.args)
        name = '{}.{}.{}'.format(message.server, message.channel, name)

        try:
            del self.tasks[name]
            await self.client.say('The task "{}" has been unscheduled.'.format(message.args))
        except:
            pass

    @command(perm=['manage_messages'])
    async def add(self, message):
        name, delay, rest = parse_cmd(message.args)
        group, cmd, args = parse_cmd(rest)
        sdelay = humanfriendly.parse_timespan(delay)

        original_command = message.args
        full_name = '{}.{}.{}'.format(message.server, message.channel, name)

        if full_name in self.tasks:
            await self.client.say('This task already exists: {}'.format(self.tasks[full_name]))
            return

        message.group = group
        message.cmd = cmd
        message.args = args

        async def do_task():
            await self.client.exec_command(message)
            await asyncio.sleep(sdelay)

            if full_name in self.tasks:
                asyncio.ensure_future(do_task())

        loop = asyncio.get_event_loop()
        future = asyncio.Future()
        asyncio.ensure_future(do_task())

        self.tasks[full_name] = original_command

        await self.client.say(
            'The task "{}" has been scheduled to be run every {}.'.format(name, delay)
        )

        try:
            loop.run_forever()
        except:
            pass

bot = ScheduleBot
