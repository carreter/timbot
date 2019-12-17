""" Module defining the base classes used to define commands. """

from __future__ import annotations
from discord import Message

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

    async def run_command(self, config: dict, message: Message) -> dict:
        """
        Invokes the function associated with the command with a new Context object
        as the argument.
        """
        new_config = await self._command_function(config, Context(config, message)) # Call the command's function
        if not new_config: # If no config was returned from command, return the old config
            return config
        else:
            return new_config

    async def _command_function(self, config: dict, ctx: Context) -> dict:
        """
        This is the function that is run when a command is invoked.
        The Context object contains all relevant info.
        """
        raise NotImplementedError