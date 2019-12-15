# timbot

`timbot` is a bot for the MIT Class of 2024 based on [discord.py](https://github.com/Rapptz/discord.py)

## Features:

## Setup:

Very simple example setup:

```python
import discord
import logging
import timbot
import commands

logging.basicConfig(level=logging.INFO)

tim = timbot.TimBot(guild_ID = <your guild ID here>)
tim.add_command(commands.PingCommand())
self_assignable_roles = ['test role 1', 'test role 2']
tim.add_command(commands.RolesCommand(self_assignable_roles))

tim.run('<your bot client token here>')
```

## Contributing:

Please make all development commits to the `devel` branch. If you're implementing a major new feature, branch off of `devel` to do so.
