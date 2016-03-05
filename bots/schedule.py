import asyncio
from config import config
import copy
from discord.errors import InvalidArgument
from humanfriendly import format_timespan
import os
import pickle

from shuckle.command import command
from shuckle.data import FileLock
from shuckle.error import ShuckleError
from shuckle.frame import Frame
from shuckle.types import Timespan
from shuckle.util import gen_help, flatten

class Task(object):
    def __init__(self, name, task, frame):
        self.server = frame.server
        self.channel = frame.channel
        self.name = name
        self.frame = frame
        self.task = task

class TaskTable(object):
    def __init__(self, tasks={}):
        self.tasks = tasks

    def add_task(self, task):
        server = task.server.id
        channel = task.channel.id
        name = task.name

        if server not in self.tasks:
            self.tasks[server] = {}

        if channel not in self.tasks[server]:
            self.tasks[server][channel] = {}

        if name in self.tasks[server][channel]:
            raise ShuckleError('This task already exists.')

        self.tasks[server][channel][name] = task

    def delete_task(self, server, channel, name):
        if hasattr(server, 'id'):
            server = server.id
        if hasattr(channel, 'id'):
            channel = channel.id

        try:
            del self.tasks[server][channel][name]
        except KeyError:
            return False
        return True

    def get_task(self, server, channel, name):
        if hasattr(server, 'id'):
            server = server.id
        if hasattr(channel, 'id'):
            channel = channel.id

        try:
            return self.tasks[server][channel][name]
        except KeyError:
            return None

    def list_tasks(self, server, channel):
        if hasattr(server, 'id'):
            server = server.id
        if hasattr(channel, 'id'):
            channel = channel.id

        try:
            return self.tasks[server][channel].items()
        except KeyError:
            return []

class ScheduleBot(object):
    '''
    **Schedule Bot**
    Provides commands for scheduling tasks to run periodically.
    '''
    __group__ = 'schedule'

    def __init__(self, client):
        self.client = client
        # Suppress all bot messages
        # while loading task schedule.
        self.announce = True
        self.tasks = TaskTable()

    async def setup(self):
        self.announce = False
        table_path = os.path.join(self.client.__DATA__, 'task_table.shuckle')

        if not os.path.isfile(table_path):
            return

        with open(table_path, 'rb') as f:
            try:
                ghost_table = pickle.load(f)
            except:
                return

        if ghost_table:
            for task in ghost_table:
                await self.client.exec_command(task)

        self.announce = True

    def teardown(self):
        save_schedule()
        self.tasks = TaskTable()

    @command()
    async def help(self):
        '''
        Show schedule commands:
        ```
        @{bot_name} schedule help
        ```
        '''
        await self.client.say(gen_help(self).format(bot_name=self.client.user.name))

    @command(perm=['manage_messages'])
    async def list(self, frame: Frame):
        '''
        Lists all scheduled tasks to run in the current chanenl [U:MM]:
        ```
        @{bot_name} schedule list
        ```
        '''
        server, channel = frame.server.id, frame.channel.id
        task_list = map(lambda x: '{}: {}'.format(x[0], x[1].task), self.tasks.list_tasks(server, channel))
        task_list = '\n'.join(task_list)
        await self.client.say('Here is a list of scheduled tasks: \n{}'.format(task_list))

    @command(perm=['manage_messages'])
    async def delete(self, frame: Frame, task: str):
        '''
        Removes a task from the scheduler [U:MM]:
        ```
        @{bot_name} schedule delete <task name>
        ```
        '''
        if not self.tasks.delete_task(frame.server, frame.channel, task):
            raise ShuckleError('This task does not exist.')

        self.save_schedule()
        await self.client.say('The task "{}" has been unscheduled.'.format(task))

    @command(perm=['manage_messages'])
    async def add(self, frame: Frame, name: str, delay: Timespan, command):
        '''
        Adds a task to run at a set interval [U:MM]:
        ```
        @{bot_name} schedule add <task name> <interval> <command (no prefix)>
        ```
        '''
        original_command = frame.message
        original_frame = copy.deepcopy(frame)

        frame.message = ' '.join(command)
        delay = delay.duration

        if delay < config.min_delay:
            raise ShuckleError('You must choose a longer interval.')
        if frame.message.startswith('schedule add'):
            raise ShuckleError('You may not schedule a recursive command.')

        if self.tasks.get_task(frame.server, frame.channel, name):
            raise ShuckleError('This task already exists.')

        async def do_task():
            await self.client.exec_command(frame)
            await asyncio.sleep(delay)

            if self.tasks.get_task(frame.server, frame.channel, name):
                asyncio.ensure_future(do_task())

        loop = asyncio.get_event_loop()
        task = Task(name, original_command, original_frame)

        asyncio.ensure_future(do_task())
        self.tasks.add_task(task)
        self.save_schedule()

        if self.announce:
            await self.client.say(
                'The task "{}" has been scheduled to be run every {}.'.format(
                    name, format_timespan(delay)
                )
            )

        try:
            loop.run_forever()
        except:
            pass

    def save_schedule(self):
        table_path = os.path.join(self.client.__DATA__, 'task_table.shuckle')
        flat_table = flatten(self.tasks.tasks)

        pickle_data = []

        for task in flat_table:
            pickle_data.append(task.frame)

        with FileLock(table_path, 'wb+') as f:
            pickle.dump(pickle_data, f, pickle.HIGHEST_PROTOCOL)

bot = ScheduleBot
