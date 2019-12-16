""" Module defining the TimBot class."""

from __future__ import annotations
import discord
from typing import List
import logging
import copy

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
    def add_command(self, command: BotCommand ):
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
                await command.run_command(self.config, message)


class Context():
    """ Object to hold information passed to a command. """
    def __init__(self, config: dict, message: Message):
        self.message = message
        self.guild = message.guild
        self.channel = message.channel
        self.config = config
        self.author = message.author

        # Remove prefix from message and split into list for args
        args = message.content[len(config['bot']['prefix']):].split()
        if len(args) > 1:
            self.args = args[1:]
        else:
            self.args = None

class CommandHelp():
    """ Object to hold help info for a command """
    pass

class BotCommand():
    """
    A command that should be run upon invocation by a user. Extend this class and define the
    _command_function method to create new commands.
    """
    def __init__(self, name: str, command_help: CommandHelp, command_function: function = None):
        self._name = name
        self._help = command_help

        if command_function:
            self._command_function = command_function

    @property
    def name(self) -> str:
        """ Returns name of the command. """
        return self._name

    @property
    def help(self) -> str:
        """ Returns the help of the command as a Discord-message formatted string. """
        return self._help.discord_formatted()

    async def run_command(self, config: dict, message: Message):
        """
        Invokes the function associated with the command with a new Context object
        as the argument.
        """
        await self._command_function(Context(config, message))

    async def _command_function(self, ctx: Context):
        """
        This is the function that is run when a command is invoked.
        The Context object contains all relevant info.
        """
        raise NotImplementedError
