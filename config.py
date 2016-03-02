DESCRIPTION = """
**{bot_name}**
Author: Reticence
Language: Python 3.5.1
Library: discord.py 0.9.2
Uptime: {uptime}

Shuckle combines many small bots into one super bot!

__Installed Modules:__
{bot_list}

Want bot specific information? Use: `@{bot_name} info|help|about <module>`
Want to see the permission glossery? Use: `@{bot_name} info|help|about permissions`
"""

POLL = """
__Poll Commands:__

Create a new poll in the current channel:
```
@{bot_name} poll make {{
    "title": <string>,
    "duration": <integer|seconds>,
    "options": [<string>]
}}
```
Shorthand for the above (does not support colons in options):
```
@{bot_name} poll make <title>:<duration>:<option>[:<option>]
```
Cast your vote for the current poll:
```
@{bot_name} poll vote <integer>
```
Delete the current poll and don't show the results [U:MM]:
```
@{bot_name} poll delete
```
"""

MOD = """
__Mod Commands:__

Deletes all messages in a channel (potentially slow) [B:MM/B:H/U:MM/U:H]:
```
@{bot_name} mod clear
```
Saves all previous messages in a text file and sends it to the user (15 MB max archive size; potentially slow) [B:MM/B:H/U:MM/U:H]
```
@{bot_name} mod archive
```
Prunes all messages by a user [B:MM/U:MM]:
```
@{bot_name} mod prune <@user>
```
"""

PERMISSIONS = """
__Permission Legend:__

B: - Bot permission
U: - User permission
MM - Manage messages
H - View message history
"""

STATS_DETAIL = """
__Stats for Geeks__
Uptime: {uptime}
Total Memory: {total_mem}
Used Memory: {used_mem}
Connected Servers: {server_count}
"""

PREFIX = '~'

BOTS_FOLDER = 'bots'

# DO NOT TOUCH ANYTHING BELOW

DESCRIPTION = DESCRIPTION.strip()
POLL = POLL.strip()
MOD = MOD.strip()
PERMISSIONS = PERMISSIONS.strip()
STATS_DETAIL = STATS_DETAIL.strip()