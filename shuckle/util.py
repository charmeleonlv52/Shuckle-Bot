import inspect
import re
from textwrap import dedent

GENERIC_HELP = '''
{class_doc}

__Command List:__

{commands}
'''

def get_internal(name):
    '''
    Returns the value of a Shuckle internal variable.
    This should only be used by the Shuckle core.
    '''
    stack = inspect.stack()

    try:
        for frame in stack:
            frame = frame[0].f_locals

            if name in frame:
                return frame[name]

        return None
    except:
        pass

def gen_help(bot):
    '''
    Generates help message text for a given bot
    using a bot's command docstrings.
    '''
    commands = []

    for x in dir(bot):
        if hasattr(getattr(bot, x), '_shuckle_command'):
            commands.append(dedent(getattr(bot, x).__doc__).strip())

    return GENERIC_HELP.strip().format(
        class_doc=dedent(bot.__doc__).strip(),
        commands=dedent('\n'.join(commands))
    )

def flatten(d):
    '''
    Flattens a multi-level dictionary into
    a single dimension list.
    '''
    flat = []

    for key in d:
        if isinstance(d[key], dict):
            flat.extend(flatten(d[key]))
        else:
            flat.append(d[key])

    return flat

def get_id(s):
    '''
    Returns an ID extracted from mention text.
    '''
    match = re.search(r'<@(\d+?)>', s)
    return match.group(1)
