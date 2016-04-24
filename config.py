config = {
    'description':
        """
        **{bot_name}**
        Author: Reticence
        Language: Python 3.5.1
        Library: discord.py async beta
        Uptime: {uptime}

        {bot_name} combines many small bots into one super bot and can be called using `@{bot_name}` or `{prefix}`.

        __Installed Modules:__
        {bot_list}

        Want module specific information? Use: `@{bot_name} <module> help`
        Want to see the permission glossery? Use: `@{bot_name} help|about|info permissions`
        Want to use {bot_name} on your own server? PM {bot_name} anything for an auth URL.
        """,
    'permissions':
        """
        __Permission Legend:__

        B: - Bot permission
        U: - User permission
        AF - Attach files
        H - View message history
        MC - Manage channels
        MM - Manage messages
        """,
    'prefix': '~',
    'bots_folder': 'bots',
    'min_delay': 5,
    'owner_id': '126383697929699328',
    'secrets_path': '../secrets.json',
    # Frozen modules cannot be disabled through Module Bot.
    'frozen_modules': ['help', 'info', 'about', 'module'],
    'mashape_key': 'uAN2N2GQYYmshZq6F4beo3U0KWVLp1b3ydQjsnHcjwFV6v0LZN'
}

# DO NOT TOUCH ANYTHING BELOW

from object import Object
from textwrap import dedent

for x in config:
    if type(config[x]) is str:
        config[x] = dedent(config[x]).strip()

config = Object(config)
