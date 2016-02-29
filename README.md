Shuckle Bot
===

Author: Reticence

Language: Python 3.5.1

Library: discord.py 0.9.2

Uptime: {uptime}

__Commands:__

Show bot description:
```
@Shuckle Bot info|help|about
```
Create a new poll in the current channel:
```
@Shuckle Bot poll make {
    "title": <string>,
    "duration": <integer|seconds>,
    "options": [<string>]
}
```
Shorthand for the above (does not support colons in options):
```
@Shuckle Bot poll make <title>:<duration|seconds>:<option>[:<option>]
```
Cast your vote for the current poll:
```
@Shuckle Bot poll vote <integer>
```
Delete the current poll and don't show the results (requires the ability to manage messages)
```
@Shuckle Bot poll delete
```
Deletes all messages in a channel (requires the ability to manage messages and read message history)
```
@Shuckle Bot mod clear
```