import discord

from discord.ext import commands

# Provides Hot-Configurable User Authentication
class AuthConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(AuthConfig(bot))

def teardown(bot):
    pass