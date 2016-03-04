import asyncio
import humanfriendly
from shuckle.command import command, parse_cmd
from shuckle.error import ShuckleError
from shuckle.util import gen_help

class Task(object):
    def __init__(self, server, channel, name, task=None):
        self.server = server
        self.channel = channel
        self.name = name
        self.task = task

class TaskTable(object):
    def __init__(self):
        self.tasks = {}

    def add_task(self, task):
        server = task.server
        channel = task.channel
        name = task.name
        task = task.task

        if server not in self.tasks:
            self.tasks[server] = {}

        if channel not in self.tasks[server]:
            self.tasks[server][channel] = {}

        if name in self.tasks[server][channel]:
            raise ShuckleError('This task already exists.')

        self.tasks[server][channel][name] = task

    def delete_task(self, task):
        try:
            del self.tasks[task.server][task.channel][task.name]
        except KeyError:
            raise ShuckleError('This task does not exist.')

    def get_task(self, server, channel, name):
        try:
            return self.tasks[server][channel][name]
        except KeyError:
            return None

    def list_tasks(self, server, channel):
        try:
            return self.tasks[server][channel].items()
        except KeyError:
            return []

class ScheduleBot(object):
    '''
    **Schedule Bot**
    Provides commands to schedule periodic tasks to run.
    '''
    __group__ = 'schedule'

    def __init__(self, client):
        self.client = client
        self.tasks = TaskTable()

    @command()
    async def help(self, frame):
        '''
        Show schedule commands:
        ```
        @{bot_name} schedule help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command(perm=['manage_messages'])
    async def list(self, frame):
        '''
        Lists all scheduled tasks to run in the current chanenl [U:MM]:
        ```
        @{bot_name} schedule list
        ```
        '''
        server, channel = frame.server, frame.channel
        task_list = map(lambda x, y: '{}: {}'.format(x, y), self.tasks.list_tasks(server, channel))
        task_list = '\n'.join(task_list)
        await self.client.say('Here is a list of scheduled tasks: \n{}'.format(task_list))

    @command(perm=['manage_messages'])
    async def delete(self, frame):
        '''
        Removes a task from the scheduler [U:MM]:
        ```
        @{bot_name} schedule delete <task name>
        ```
        '''
        task = Task(frame.server, frame.channel, frame.args)
        self.tasks.delete_task(task)
        await self.client.say('The task "{}" has been unscheduled.'.format(frame.args))

    @command(perm=['manage_messages'])
    async def add(self, frame):
        '''
        Adds a task to run at a set interval [U:MM]:
        ```
        @{bot_name} schedule add <task name> <interval> <command (no prefix)>
        ```
        '''
        name, delay, rest = parse_cmd(frame.args)
        group, cmd, args = parse_cmd(rest)
        sdelay = humanfriendly.parse_timespan(delay)

        original_command = frame.args

        if self.tasks.get_task(frame.server, frame.channel, name):
            await self.client.say('This task already exists.')
            return

        frame.group = group
        frame.cmd = cmd
        frame.args = args

        async def do_task():
            await self.client.exec_command(frame)
            await asyncio.sleep(sdelay)

            if self.tasks.get_task(frame.server, frame.channel, name):
                asyncio.ensure_future(do_task())

        loop = asyncio.get_event_loop()
        asyncio.ensure_future(do_task())

        task = Task(frame.server, frame.channel, name, original_command)
        self.tasks.add_task(task)

        await self.client.say('The task "{}" has been scheduled to be run every {}.'.format(name, delay))

        try:
            loop.run_forever()
        except:
            pass

bot = ScheduleBot
