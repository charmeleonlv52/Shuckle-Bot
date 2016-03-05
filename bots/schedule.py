import asyncio
import copy
from discord.errors import InvalidArgument
from humanfriendly import format_timespan
import os

from config import config

from shuckle.command import command
from shuckle.data import FileLock
from shuckle.error import ShuckleError
from shuckle.frame import Frame
from shuckle.schedule import load_schedule, add_task, delete_task, get_task, list_tasks
from shuckle.types import Timespan
from shuckle.util import gen_help, flatten

class Task(object):
    def __init__(self, name, command, frame):
        self.channel = frame.channel
        self.name = name
        self.invoke_command = command
        self.frame = frame

class ScheduleBot(object):
    '''
    **Schedule Bot**
    Provides commands for scheduling tasks to run periodically.
    '''
    __group__ = 'schedule'

    def __init__(self, client):
        self.client = client
        self.loaded = False

    async def setup(self):
        ghost_table = load_schedule()

        if ghost_table:
            for task in ghost_table:
                await self.client.exec_command(task.frame)

        self.loaded = True

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
        task_list = [x.task for x in list_tasks(frame.channel.id)]
        task_list = map(lambda x: '{}: {}'.format(x.name, x.invoke_command), task_list)
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
        if not delete_task(frame.channel.id, task):
            raise ShuckleError('This task does not exist.')

        await self.client.say('The task "{}" has been unscheduled.'.format(task))

    @command(perm=['manage_messages'])
    async def add(self, frame: Frame, name: str, delay: Timespan, command):
        '''
        Adds a task to run at a set interval [U:MM]:
        ```
        @{bot_name} schedule add <task name> <interval> <command (no prefix)>
        ```
        '''
        original_frame = copy.deepcopy(frame)

        frame.message = ' '.join(command)

        if delay < config.min_delay:
            raise ShuckleError('You must choose a longer interval.')
        if frame.message.startswith('schedule add'):
            raise ShuckleError('You may not schedule a recursive command.')

        if self.loaded and get_task(frame.channel.id, name):
            raise ShuckleError('This task already exists.')

        async def do_task():
            await self.client.exec_command(frame)
            await asyncio.sleep(delay)

            if self.tasks.get_task(frame.server, frame.channel, name):
                asyncio.ensure_future(do_task())

        task = Task(name, frame.message, original_frame)

        if not add_task(task):
            raise ShuckleError('Unable to schedule task.')

        if self.announce:
            await self.client.say(
                'The task "{}" has been scheduled to be run every {}.'.format(
                    name, format_timespan(delay)
                )
            )

        try:
            loop = asyncio.get_event_loop()
            asyncio.ensure_future(do_task())
            loop.run_forever()
        except:
            pass

bot = ScheduleBot
