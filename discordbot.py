import discord
import json

from discord.ext import commands

def PermCheck(ctx):
    # get authorized roles
    cog_perms = ctx.bot.perms['cogs'][ctx.command.cog_name]
    authorized_roles = set(cog_perms[ctx.command.name] if ctx.command.name in cog_perms else cog_perms['__default__'])

    # if there are no roles, allow anyone
    if not authorized_roles: return True

    # get the author's roles
    author_roles = set([role.id for role in ctx.message.author.roles])

    # get whitelist values
    try:
        author_roles.update(ctx.bot.perms['whitelist'][str(ctx.message.author.id)])
    except KeyError:
        pass

    # return True if there is an intersection with the authorized roles
    return bool(authorized_roles.intersection(author_roles))

class Bot(commands.Bot):
    def __init__(self, command_prefix, perm_path=None, help_command=commands.bot._default, description=None, **options):
        super().__init__(command_prefix, help_command=help_command, description=description, **options)
        self.perm_path = perm_path
        self.load_perms()

    def load_perms(self):
        with open(self.perm_path) as f:
            self.perms = json.load(f)
    
    def save_perms(self):
        with open(self.perm_path, 'w') as f:
            json.dump(self.perms, f)