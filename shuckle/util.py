import inspect
from textwrap import dedent

GENERIC_HELP = '''
{class_doc}

__Command List:__

{commands}
'''

def get_internal(name):
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
    commands = []

    for x in dir(bot):
        if hasattr(getattr(bot, x), '_shuckle_command'):
            commands.append(dedent(getattr(bot, x).__doc__).strip())

    return GENERIC_HELP.strip().format(
        class_doc=dedent(bot.__doc__).strip(),
        commands=dedent('\n'.join(commands))
    )
