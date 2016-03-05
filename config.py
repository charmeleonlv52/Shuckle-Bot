config = {
    'description':
        """
        **{bot_name}**
        Author: Reticence
        Language: Python 3.5.1
        Library: discord.py async beta
        Uptime: {uptime}

        Shuckle combines many small bots into one super bot!

        __Installed Modules:__
        {bot_list}

        Want module specific information? Use: `@{bot_name} <module> help`
        Want to see the permission glossery? Use: `@{bot_name} help|about|info permissions`
        """,
    'permissions':
        """
        __Permission Legend:__

        B: - Bot permission
        U: - User permission
        AF - Attach files
        MM - Manage messages
        H - View message history
        """,
    'prefix': '~',
    'bots_folder': 'bots',
    'min_delay': 5,
    'owner_id': '126383697929699328',
    'secrets_path': '../secrets.json'
}

# DO NOT TOUCH ANYTHING BELOW

from object import Object
from textwrap import dedent

for x in config:
    if type(config[x]) is str:
        config[x] = dedent(config[x]).strip()

config = Object(config)
