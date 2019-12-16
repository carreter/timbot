""" Role management commands. """
from timbot.commands import BotCommand, Context, CommandHelp
import discord.utils
import asyncio

class RolesCommand(BotCommand):
    """
    Command to self-assign roles.

    TODO: Implement ability to change self-assign status of roles on the fly.
    """
    def __init__(self):
        """
        Create RolesCommand object.

        self_assignable_roles: List of roles that can be self-assigned.
        """
        name = 'roles'
        command_help = CommandHelp()

        super().__init__(name, command_help)

    async def _print_roles(self, roles, channel):
        """ 
        Creates Discord-formatted representation of self-assignable roles
        and sends it in channel.
        """
        role_message = 'List of self-assignable roles: \n------------------------------\n```'

        for role in roles:
            role_message += '{}\n'.format(role)

        role_message += '```'

        await channel.send(role_message)

    async def _assign_role(self, role_name: str, member: discord.Member, channel: discord.TextChannel):
        """
        Assigns role to member.
        Prints success/failure in channel.
        """
        # TODO: check if user has/doesn't have role in the first place
        role = discord.utils.get(channel.guild.roles, name = role_name) # Get the role object
        await member.add_roles(role) # Assign the role

        await asyncio.sleep(.5) # Wait before checking that role was successfully added
        if role in member.roles: # Verify that role is assigned
            await channel.send('Role `{}` successfully assigned!'.format(role_name))
        else:
            await channel.send('Role `{}` could not be assigned. Try again.'.format(role_name))

    async def _remove_role(self, role_name: str, member: discord.Member, channel: discord.TextChannel):
        """
        Removes role from member.
        Prints success/failure in channel.
        """
        # TODO: check if user has/doesn't have role in the first place
        role = discord.utils.get(channel.guild.roles, name = role_name) # Get the role object
        await member.remove_roles(role) # Assign the role

        await asyncio.sleep(.5) # Wait before checking that role was successfully removed
        if not role in member.roles: # Verify that role is removed
            await channel.send('Role `{}` successfully removed!'.format(role_name))
        else:
            await channel.send('Role `{}` could not be removed. Try again.'.format(role_name))

    async def _command_function(self, config: dict, ctx: Context):
        if not ctx.args:
            return await ctx.channel.send('Roles command must be run with argument `list`, `iam`, or `iamnot`.')

        sub_command = ctx.args[0]
        role_name = ' '.join(ctx.args[1:])
        self_assignable_roles = config[self.name]['self_assignable_roles']

        if sub_command == 'list':
            await self._print_roles(self_assignable_roles, ctx.channel)
        elif sub_command == 'iam':
            if role_name in self_assignable_roles: # Check that a role is listed as assignable
                await self._assign_role(role_name, ctx.author, ctx.channel)
            else:
                await ctx.channel.send('`{}` is not a self-assignable role!'.format(role_name))
        elif sub_command == 'iamnot':
            if role_name in self_assignable_roles: # Check that a role is listed as assignable
                await self._remove_role(role_name, ctx.author, ctx.channel)
            else:
                await ctx.channel.send('`{}` is not a self-assignable role!'.format(role_name))
        else:
            await ctx.channel.send('Unrecognized roles command `{}`. Please try `list`, `iam`, or `iamnot`.'.format(sub_command))