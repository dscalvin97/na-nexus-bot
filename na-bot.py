import discord
import json
import traceback
import sys

from discord.ext import commands

# bot initialization
bot = commands.Bot(command_prefix='$', case_insensitive=True)

# list of cogs to be loaded
initial_extensions = ['cogs.modulemgr', 'cogs.greeting', 'cogs.rolemgr']#, 'cogs.role-management']

# loading of cogs
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f'{extension} loaded')
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}\nWith ID: {bot.user.id}')
    return await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for screams of agony'))

# ping
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# used to clean up messages with matching content(not working yet)
@bot.command()
async def Cleanup(ctx, targetMessage):
    for message in ctx.message.channel.history():
        if message.content == targetMessage:
            print(targetMessage.id)
        else:
            print("Not found")

# load token from config file(will later come to include other important data, like webhook tokens, etc.)
with open('config.json') as config_file:
    data = json.load(config_file)
TOKEN = data["token"]

bot.run(TOKEN)
