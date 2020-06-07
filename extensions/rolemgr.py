import discord

from discord import user
from discord.ext import commands
from discord.utils import get
from datetime import datetime

# provides commands to get statistical data for roles
class RoleStatistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # post an embed with a count of members in all roles for the server
    @commands.command()
    async def RoleCount(self, ctx, ignoreBots=True):
        embed = discord.Embed(title="Roles", color=0x7289da)

        for role in ctx.guild.roles:
            role_name = role.name
            
            if role.name == "@everyone":
                role_name = "Total members"

            embed.add_field(name=f"{role_name} :", inline=True, value=len(role.members))

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(RoleStatistics(bot))

def teardown(bot):
    pass