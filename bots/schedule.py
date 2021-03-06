import asyncio
import copy
from discord.errors import InvalidArgument
from humanfriendly import format_timespan
import os
import traceback

from config import config

from shuckle.command import command
from shuckle.error import ShuckleError
from shuckle.frame import Frame
from shuckle.db.schedule import load_schedule, add_task, delete_task, get_task, list_tasks
from shuckle.types import Timespan
from shuckle.util import gen_help

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

    @command(perm=['manage_messages', 'manage_channels'])
    async def list(self, frame: Frame):
        '''
        Lists all scheduled tasks to run in the current chanenl [U:MC/U:MM]:
        ```
        @{bot_name} schedule list
        ```
        '''
        task_list = [x.task for x in list_tasks(frame.channel.id)]
        task_list = map(lambda x: '{}: {}'.format(x.name, x.invoke_command), task_list)
        task_list = '\n'.join(task_list)

        await self.client.say('Here is a list of scheduled tasks: \n{}'.format(task_list))

    @command(perm=['manage_messages', 'manage_channels'])
    async def delete(self, frame: Frame, task: str):
        '''
        Removes a task from the scheduler [U:MC/U:MM]:
        ```
        @{bot_name} schedule delete <task name>
        ```
        '''
        if not delete_task(frame.channel.id, task):
            raise ShuckleError('This task does not exist.')

        await self.client.say('The task **{}** has been unscheduled.'.format(task))

    @command(perm=['manage_messages', 'manage_channels'])
    async def add(self, frame: Frame, name: str, delay: Timespan, command):
        '''
        Adds a task to run at a set interval [U:MC/U:MM]:
        ```
        @{bot_name} schedule add <task name> <interval> <command (no prefix)>
        ```
        '''
        original_frame = copy.deepcopy(frame)
        original_message = frame.message

        frame.message = ' '.join(command)

        if delay < config.min_delay:
            raise ShuckleError('You must choose a longer interval.')
        if frame.message.startswith('schedule add'):
            raise ShuckleError('You may not schedule a recursive command.')

        # self.loaded is False if we're currently running
        # setup. In which case, we should not announce when
        # a task has been scheduled.
        task = Task(name, original_message, original_frame)

        if self.loaded:
            if get_task(frame.channel.id, name):
                raise ShuckleError('This task already exists.')
            elif not add_task(task):
                raise ShuckleError('Unable to schedule task.')

            await self.client.say(
                'Okay. I will run the task **{}** every {}.'.format(
                    name, format_timespan(delay)
                )
            )

        async def do_task():
            try:
                while get_task(frame.channel.id, name):
                    await self.client.exec_command(frame)
                    await asyncio.sleep(delay)
            except:
                traceback.print_exc()

        loop = asyncio.get_event_loop()
        asyncio.ensure_future(do_task())

bot = ScheduleBot
