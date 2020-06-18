import discord
from discord.ext import commands


# commands to get statistical data for roles
class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # post an embed with a count of members in all roles for the server
    @commands.command()
    async def RoleCount(self, ctx):
        embed = discord.Embed(title="Roles", color=0x7289DA)

        for role in ctx.guild.roles:
            role_name = role.name

            if role.name == "@everyone":
                role_name = "Total members"

            embed.add_field(name=f"{role_name} :", inline=True, value=len(role.members))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Statistics(bot))