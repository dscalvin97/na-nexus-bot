import discord
from tinydb import TinyDB, where

from discord.ext import commands


def PermCheck(ctx):
    # override for owner in case of error
    if commands.is_owner():
        return True

    # get permissions tables
    command_perms = ctx.bot.db.table('permissions-command')
    cogs = ctx.bot.db.table('permissions-cogs')
    overrides = ctx.bot.db.table('permissions-overrides')

    # get authorized roles and allow anyone if there are none
    command = command_perms.get(where('name') == ctx.command.name)
    if not command:
        command = cogs.get(where('name') == ctx.command.cog_name)
        if not command:
            return True
    authorized_roles = set(command['roles'])

    # if there are no roles, allow anyone
    if not authorized_roles:
        return True

    # get the author's roles
    author_roles = set([role.id for role in ctx.message.author.roles])

    # get whitelist values
    author_overrides = overrides.get(where('user') == ctx.message.author.id)
    if author_overrides:
        author_roles.update(author_overrides['roles'])

    # return True if there is an intersection with the authorized roles
    return bool(authorized_roles.intersection(author_roles))


class Bot(commands.Bot):
    def __init__(self, database: TinyDB, command_prefix, help_command=commands.bot._default, description=None, **options):
        super().__init__(command_prefix, help_command=help_command,
                         description=description, **options)
        self.db = database
