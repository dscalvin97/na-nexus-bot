import discord

from discord.ext import commands

# cog to manage usage and functioning of other cogs and extensions when bot is running
class ModuleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load an inactive extension
    @commands.command()
    async def LoadCog(self, ctx, cogName):
        ctx.author.send(f"Loading Cog {cogName}")
        try:
            self.bot.load_extension(cogName)
            await ctx.author.send(f'{cogName} loaded')
        except Exception as e:
            await ctx.author.send(f'Failed to load Cog {cogName}\n{e}')

    # Unload an active extension
    @commands.command()
    async def UnloadCog(self, ctx, cogName):
        pass

def setup(bot):
    bot.add_cog(ModuleManager(bot))
    