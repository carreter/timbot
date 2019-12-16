""" Module defining the TimBot class."""

from __future__ import annotations
import discord
from typing import List
import logging
import copy
from timbot.commands.core import BotCommand

LOGGER = logging.getLogger(__name__)

class TimBot(discord.Client):
    def __init__(self, config: dict, **options):
        super().__init__(**options) # Create a discord client object

        self._guild_ID = config['bot']['guild_ID'] # Get the main guild the bot instance is to be run on
        
        prefix = config['bot'].get('prefix', None) # Get prefix setting
        if not prefix: # Default prefix if not set: '!'
            prefix = '!'
            config['bot']['prefix'] = prefix
        self._prefix = prefix

        self._commands = {} # Initialize empty commands dict
        self._config = copy.deepcopy(config) # Save config on the bot instance

    # Getters and setters here
    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def config(self) -> dict:
        return copy.deepcopy(self._config)

    # Bot configuration
    def add_command(self, command: BotCommand):
        """
        Registers a command (type BotCommand) with TimBot.
        """
        if command.name in self._commands.keys():
            raise ValueError('Command with name {} already registered!'.format(command.name))

        self._commands[command.name] = command

    # Events
    async def on_ready(self):
        """ Runs after bot is started up and ready. """
        await self.wait_until_ready()
        self._guild = self.get_guild(self._guild_ID)

        LOGGER.info('Ready!')

    async def on_message(self, message: discord.Message):
        """ Runs each time a message is sent. """
        if message.guild != self._guild:
            return

        if message.content.startswith(self._prefix):
            command_name = message.content[len(self._prefix):].split() [0] # Get the name of command that was run

            command = self._commands.get(command_name, None)

            if command:
                self._config = await command.run_command(self.config, message)

