import asyncio
import copy
import humanfriendly
import json
import os
import pickle
from shuckle.command import command, parse_cmd
from shuckle.data import read_binary, write_binary
from shuckle.error import ShuckleError
from shuckle.util import gen_help

class Task(object):
    def __init__(self, server, channel, name, frame, task=None):
        self.server = server
        self.channel = channel
        self.name = name
        self.task = task
        self.frame = frame

class TaskTable(object):
    def __init__(self, tasks={}):
        self.tasks = tasks

    def add_task(self, task):
        server = task.server.name
        channel = task.channel.name
        name = task.name

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

    def setup(self):
        table_path = os.path.join(self.client.__DATA__, 'task_table.json')

        if not os.path.isfile(table_task):
            return

        contents = read_binary(table_path)

        if contents:
            ghost_table = pickle.loads(contents)

            for server in ghost_table.tasks:
                for channel in ghost_table.tasks[server]:
                    for task in ghost_table.tasks[server][channel]:
                        self.add_task(task.frame)

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
        server, channel = frame.server.name, frame.channel.name
        task_list = map(lambda x: '{}: {}'.format(x[0], x[1]), self.tasks.list_tasks(server, channel))
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
        task = Task(frame.server, frame.channel, frame.args, frame)
        self.tasks.delete_task(task)

        await self.save_schedule()
        await self.client.say('The task "{}" has been unscheduled.'.format(frame.args))

    @command(perm=['manage_messages'])
    async def add(self, frame):
        '''
        Adds a task to run at a set interval [U:MM]:
        ```
        @{bot_name} schedule add <task name> <interval> <command (no prefix)>
        ```
        '''
        original_frame = copy.deep_copy(frame)
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
        task = Task(frame.server, frame.channel, name, origina_frame, original_command)

        asyncio.ensure_future(do_task())
        self.tasks.add_task(task)
        self.save_schedule()

        await self.client.say('The task "{}" has been scheduled to be run every {}.'.format(name, delay))

        try:
            loop.run_forever()
        except:
            pass

    def save_schedule(self):
        output = pickle.dumps(self.tasks)
        table_path = os.path.join(self.client.__DATA__, 'task_table.json')
        write_file(table_path, output)

bot = ScheduleBot
