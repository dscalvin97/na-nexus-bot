import discord
import json
from tinydb import TinyDB
import traceback
import sys
import asyncio

import discordbot


# load config file and database
db = TinyDB('database.json')
with open('config.json') as config_file:
    config = json.load(config_file)

# bot initialization
bot = discordbot.Bot(database=db, perm_path='perms.json',
                     command_prefix=config['bot-prefix'], case_insensitive=True)
bot.add_check(discordbot.PermCheck)

# list of extensions to be loaded
initial_extensions = config['extensions']

# loading of extensions
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
    return await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for howls of pain'))

TOKEN = config['token']

bot.run(TOKEN)
