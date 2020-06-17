import asyncio

import discord
from discord import Embed
from discord.ext import commands


class EmbedDetection(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_embed_information = bot.db.table("embeddetection")

    @commands.command()
    async def add_embed(self, ctx, channel: discord.TextChannel, value):
        # channel = channel in which embed should be sent,domain= the department in which the embed should be sent,value = message to be shown
        self.channel_embed_information.insert({"channel-id": channel.id, "value": value})
        await ctx.message.add_reaction('✅')

    @commands.Cog.listener()
    async def on_message(self, message):
        pic_ext = ['.jpg', '.png', '.jpeg']
        if message.attachments != []:
            for ext in pic_ext:
                attach = str(message.attachments[0])
                if attach.endswith(f"{ext}\'>"):
                    for entry in self.channel_embed_information.all():
                        if entry['channel-id'] == message.channel.id:
                            embed_to_be_sent = Embed(title="Embed Detected!", color=0xff0000)
                            embed_to_be_sent.add_field(name=f"Dearest {message.author.name},", value=entry['value'])
                            MessageInChat = await message.channel.send(embed=embed_to_be_sent)
                            await message.author.send(embed=embed_to_be_sent)
                            await asyncio.sleep(90)
                            await MessageInChat.delete()


def setup(bot):
    bot.add_cog(EmbedDetection(bot))
