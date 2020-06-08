import discord
import json

from discord.ext import commands

# Provides Hot-Configurable User Authentication
class AuthConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ViewPerms(self, ctx):
        """View Permission Json"""
        await ctx.send(f'```{json.dumps(ctx.bot.auth)}```')

def setup(bot):
    bot.add_cog(AuthConfig(bot))

def teardown(bot):
    pass