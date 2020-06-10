import discord
from tinydb import TinyDB, Query

from discord.ext import commands


def PermCheck(ctx):
    # override for owner in case of error
    if commands.is_owner():
        return true

    # get permissions tables
    commands = ctx.bot.db.table('command-permissions')
    cogs = ctx.bot.db.table('cog-permissions')
    overrides = ctx.bot.db.table('permission-overrides')
    Cog, Command, Override = Query()

    # get authorized roles
    command_perms = commands.get(Command.name == ctx.command.name)
    if not command_perms:
        command_perms = cogs.get(Cog.name == ctx.command.cog_name)
    authorized_roles = set(command_perms.roles)

    # if there are no roles, allow anyone
    if not authorized_roles:
        return True

    # get the author's roles
    author_roles = set([role.id for role in ctx.message.author.roles])

    # get whitelist values
    author_overrides = overrides.get(Override.user == ctx.message.author.id)
    author_roles.update(author_overrides.roles)

    # return True if there is an intersection with the authorized roles
    return bool(authorized_roles.intersection(author_roles))


class Bot(commands.Bot):
    def __init__(self, database: TinyDB, command_prefix, help_command=commands.bot._default, description=None, **options):
        super().__init__(command_prefix, help_command=help_command,
                         description=description, **options)
        self.db = database
