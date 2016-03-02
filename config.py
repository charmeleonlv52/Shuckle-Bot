DESCRIPTION = """
**{bot_name}**
Author: Reticence
Language: Python 3.5.1
Library: discord.py 0.9.2
Uptime: {uptime}

For a list of commands use: `@{bot_name} info|help|about commands`
For a permission legend use: `@{bot_name} info|help|about permissions`
"""

COMMANDS = """
__Commands:__

Show bot description:
```
@{bot_name} info|help|about
```
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
Deletes all messages in a channel (potentially slow) [B:MM/B:H/U:MM/U:H]:
```
@{bot_name} mod clear
```
Saves all previous messages in text file and sends it to the user (maximum of 15 MB; potentially slow) [B:MM/B:H/U:MM/U:H]
```
@{bot_name} mod archive
```
Note: The leading character "~" may be substituted for "@{bot_name}".
"""

PERMISSIONS = """
__Permission Legend:__

B: - Bot permission
U: - User permission
MM - Manage messages
H - View message history
"""

PREFIX = '~'

BOTS_FOLDER = 'bots'

# DO NOT TOUCH ANYTHING BELOW

DESCRIPTION = DESCRIPTION.strip()
COMMANDS = COMMANDS.strip()
PERMISSIONS = PERMISSIONS.strip()