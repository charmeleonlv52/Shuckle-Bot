import asyncio
import humanfriendly
from shuckle.command import command, parse_cmd
from shuckle.util import gen_help

class ScheduleBot(object):
    '''
    **Schedule Bot**
    Provides commands to schedule periodic tasks to run.
    '''
    __group__ = 'schedule'

    def __init__(self, client):
        self.client = client
        self.tasks = {}

    @command()
    async def help(self, message):
        '''
        Show schedule commands:
        ```
        @{bot_name} schedule help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command(perm=['manage_messages'])
    async def list(self, message):
        '''
        Lists all scheduled tasks to run [U:MM]:
        ```
        @{bot_name} schedule list
        ```
        '''
        task_list = []

        for task in sorted(self.tasks.keys()):
            task_list.append('{}: {}'.format(task, self.tasks[task]))

        task_list = '\n'.join(task_list)
        await self.client.say('Here is a list of scheduled tasks: \n{}'.format(task_list))

    @command(perm=['manage_messages'])
    async def delete(self, message):
        '''
        Adds a task to be run at a set interval [U:MM]:
        ```
        @{bot_name} schedule add <task name> <interval> <command (no prefix)>
        ```
        '''
        name, delay, rest = parse_cmd(message.args)
        name = '{}.{}.{}'.format(message.server, message.channel, name)

        try:
            del self.tasks[name]
            await self.client.say('The task "{}" has been unscheduled.'.format(message.args))
        except:
            pass

    @command(perm=['manage_messages'])
    async def add(self, message):
        '''
        Removes as task from the scheduler [U:MM]:
        ```
        @{bot_name} schedule delete <task name>
        ```
        '''
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
