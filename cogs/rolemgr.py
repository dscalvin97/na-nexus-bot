import discord

from discord import user
from discord.ext import commands
from discord.utils import get
from datetime import datetime

# cog to manager user roles
class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # post an ember with a count of members in all roles for the server
    @commands.command()
    async def RoleCount(self, ctx):
        mapper = 0
        # TEMP FIX 
        roles = []
        members = []
        counter = []

        # append member to members(ignores bots)
        for member in ctx.guild.members:
            if not member.bot:
                members.append(member)

        # append roleData.name to roles
        for roleData in ctx.guild.roles:
            roles.append(roleData.name)
            counter.append(0)

        # update member count for each role in counter
        for member in members:
            for memberRole in member.roles:
                counter[roles.index(memberRole.name)]+=1

        # embed counter data and post message in same channel as command channel
        embed = discord.Embed(title="Roles", color=0x7289da)
        for roleData in roles:
            roleName = roleData
            
            if roleData == "@everyone":
                roleName = "Total members"

            embed.add_field(name=f"{roleName} :", inline=True, value=counter[mapper])
            mapper+= 1

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(RoleManager(bot))
    