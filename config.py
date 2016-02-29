DESCRIPTION = """
**{bot_name}**
Author: Reticence
Language: Python 3.5.1
Library: discord.py 0.9.2
Uptime: {uptime}

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
@{bot_name} poll make <title>:<duration|seconds>:<option>[:<option>]
```
Cast your vote for the current poll:
```
@{bot_name} poll vote <integer>
```
Delete the current poll and don't show the results (requires the ability to manage messages)
```
@{bot_name} poll delete
```
Deletes all messages in a channel (requires the ability to manage messages and read message history)
```
@{bot_name} mod clear
```
"""

BOTS_FOLDER = 'bots'

# DO NOT TOUCH ANYTHING BELOW

DESCRIPTION = DESCRIPTION.strip()