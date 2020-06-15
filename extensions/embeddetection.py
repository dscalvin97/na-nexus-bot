import discord
from discord.ext import commands
from tinydb import Query, where


class EmbedDetection(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whitelist(self, ctx, type, channel: discord.TextChannel = None):
        db = ctx.bot.db.table('embeddetection-channelwhitelist')
        if type == "print":
            await ctx.send(f"`{db.all()}`")
        elif type == "add":
            if not (channel is None):
                db.insert({'channel-name': channel.name, 'channel-id': channel.id})
                await ctx.send(f"{channel.name} Has Been Added To The DataBase!")
        elif type == "remove":
            remove_query = Query()
            try:
                db.remove(remove_query['channel-name'].search(channel.name))
                await ctx.send(f"channel {channel.name} has been removed!")
            except:
                await ctx.send("Channel Not Found")

    @commands.Cog.listener()
    async def on_message(self, message):
        db = self.bot.db.table('embeddetection-channelwhitelist')
        if db.get(where('channel-id') != message.channel.id):
            pic_ext = ['.jpg', '.png', '.jpeg']
            if message.attachments != []:
                for ext in pic_ext:
                    attach = str(message.attachments[0])
                    if attach.endswith(f"{ext}\'>"):
                        await message.author.send("EMBED DETECTED")


def setup(bot):
    bot.add_cog(EmbedDetection(bot))
