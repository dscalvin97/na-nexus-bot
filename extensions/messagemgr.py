import discord

from discord.ext import commands


class MessageManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # used to delete messages with matching content
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def Cleanup(self, ctx, targetContent, msglimit=200):
        counter=0

        await ctx.message.channel.send(f'`Looking for messages that match "{targetContent}" in the last {msglimit} messages`')

        async for message in ctx.message.channel.history(limit=msglimit):
            if message.content == targetContent:
                await message.delete()
                counter+=1

        await ctx.message.channel.send(f'`{counter} out of {msglimit} messages have been deleted`')

    @Cleanup.error
    async def IncorrectParams(self, ctx, e):
        return await ctx.message.channel.send(f'`Please provide an integer for the message limit`\n`{e}`')


def setup(bot):
    bot.add_cog(MessageManager(bot))

def teardown(bot):
    pass