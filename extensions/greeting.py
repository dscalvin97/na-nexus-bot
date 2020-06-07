import discord
from discord.ext import commands
import asyncio

# interactions with those who have newly joined the server
class GreetNewUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    greetChannel=0
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_message=f"Hi there {member.name}!! We're glad to have you join us at Nexus Aurora :)"
        
        # greets members via DMs when they join
        try:
            await member.send(welcome_message)
        except Exception as error:
            if error == '403 Forbidden (error code: 50007): Cannot send messages to this user':
                if not self.greetChannel == 0:
                    await member.guild.get_channel(self.greetChannel).send(welcome_message)
                else:
                    await member.guild.system_channel.send(welcome_message)

    @commands.command(aliases=['setgreet'])
    async def SetWelcomeChannel(self, ctx):
        self.greetChannel=ctx.message.channel.id


def setup(bot):
    bot.add_cog(GreetNewUser(bot))
    