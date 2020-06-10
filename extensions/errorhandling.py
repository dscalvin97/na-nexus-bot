import discord
import sys
import math
import traceback

from discord.ext import commands


async def on_command_error(ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send('There is no such command.')

    if isinstance(error, commands.DisabledCommand):
        return await ctx.send('This command has been disabled.')

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown, please retry in {math.ceil(error.retry_after)}s.')
        return

    if isinstance(error, commands.UserInputError):
        await ctx.send(f'Invalid input. Use {ctx.bot.command_prefix}help {ctx.command.name} to see the correct usage.')
        return

    if isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.author.send('This command cannot be used in direct messages.')
        except discord.Forbidden:
            pass

    if isinstance(error, commands.CheckFailure):
        await ctx.send('You do not have permission to use this command.')
        return

    # ignore all other exception types, but print them to stderr
    print('Ignoring exception in command {}:'.format(
        ctx.command), file=sys.stderr)

    traceback.print_exception(
        type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_listener(on_command_error)


def teardown(bot):
    bot.remove_listener(on_command_error)
