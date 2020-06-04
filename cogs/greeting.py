import discord
from discord.ext import commands
import asyncio

# cog for interactions with those who have newly joined the server
class GreetNewUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # greets members via DMs when they join
        await member.send(f"Hi there {member.name}!! We're glad to have you join us at Nexus Aurora :)")

def setup(bot):
    bot.add_cog(GreetNewUser(bot))
    