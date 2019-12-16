""" Simple ping-pong command. """
from timbot.commands.core import BotCommand, Context, CommandHelp

class PingCommand(BotCommand):
    """
    Example implementation of a command that responds Pong! when it is invoked.
    Use this as a template!
    """
    def __init__(self):
        name = 'ping'
        command_help = CommandHelp()

        super().__init__(name, command_help)

    async def _command_function(self, config, ctx):
        await ctx.channel.send('Pong!')
