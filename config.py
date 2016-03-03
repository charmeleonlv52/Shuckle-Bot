DESCRIPTION = """
**{bot_name}**
Author: Reticence
Language: Python 3.5.1
Library: discord.py async beta
Uptime: {uptime}

Shuckle combines many small bots into one super bot!

__Installed Modules:__
{bot_list}

Want module specific information? Use: `@{bot_name} <module> help`
Want to see the permission glossery? Use: `@{bot_name} info|help|about permissions`
"""

PERMISSIONS = """
__Permission Legend:__

B: - Bot permission
U: - User permission
AF - Attach files
MM - Manage messages
H - View message history
"""

PREFIX = '~'
BOTS_FOLDER = 'bots'
OWNER_ID = '126383697929699328'

# DO NOT TOUCH ANYTHING BELOW

DESCRIPTION = DESCRIPTION.strip()
PERMISSIONS = PERMISSIONS.strip()
