import discord
from tinydb import TinyDB, where

from discord.ext import commands

# Provides Hot-Configurable User Authentication


class PermConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def SetOverrides(self, ctx, member: discord.Member, *roles: discord.Role):
        """Set overriden perms for Member

        Args:
            member: Member to set whitelist roles.
            roles: Roles to whitelist.
        """
        overrides = ctx.bot.db.table('permissions-overrides')
        overrides.upsert({'user': member.id, 'roles': [
                         role.id for role in roles]}, where('user') == member.id)

        await ctx.send(f'Set overrides for {member.display_name}.')

    @commands.command()
    async def SetCommandPerms(self, ctx, command_name: str, *roles: discord.Role):
        """Set roles which can run a command

        Args:
            command: Command to set permissions for.
            roles: Roles to grant permission. If you specify none, any member can run the command.
        """
        command = ctx.bot.get_command(command_name)
        command_perms = ctx.bot.db.table('permissions-commands')
        if command:
            command_perms.upsert(
                {'name': command.name, 'roles': [role.id for role in roles]}, where('name') == command.name)

            await ctx.send(f'Set permissions for command {command.name}.')
        else:
            await ctx.send(f'No such command {command_name}.')

    @commands.command()
    async def SetCogPerms(self, ctx, cog_name: str, *roles: discord.Role):
        """Set roles which can by default run commands for a cog

        Args:
            cog: Cog to set permissions for.
            roles: Roles to grant permission. If you specify none, any member can run the command.
        """
        cog = ctx.bot.get_cog(cog_name)
        cog_perms = ctx.bot.db.table('permissions-cogs')
        if cog:
            cog_perms.upsert(
                {'name': cog.qualified_name, 'roles': [role.id for role in roles]}, where('name') == cog.qualified_name)

            await ctx.send(f'Set permissions for cog {cog.qualified_name}.')
        else:
            await ctx.send(f'No such cog {cog_name}.')


def setup(bot):
    bot.add_cog(PermConfig(bot))


def teardown(bot):
    pass
