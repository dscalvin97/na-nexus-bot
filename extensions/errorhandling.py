import discord
import sys
import traceback

from discord.ext import commands

async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    
    ignored = (commands.CommandNotFound, commands.UserInputError)
    error = getattr(error, 'original', error)
    
    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.send(f'{ctx.command} can not be used in Private Messages.')
        except:
            pass

    elif isinstance(error, commands.BadArgument):
        return await ctx.send(f'You had faulty arguments. Use {ctx.bot.command_prefix}help command to see correct usage.')

    elif isinstance(error, commands.CheckFailure):
        return await ctx.send('You have insufficient permission to run this command.')
    
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_listener(on_command_error)

def teardown(bot):
    bot.remove_listener(on_command_error)