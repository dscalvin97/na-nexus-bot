import discord
from discord.ext import commands
from tinydb import Query, where


class EmbedDetection(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_whitelist = bot.db.table('embeddetection')


    @commands.command()
    async def whitelist(self, ctx, type, channel: discord.TextChannel = None):

        if type == "add":
            if not (channel is None):
                self.channel_whitelist.insert({'channel-name': channel.name, 'channel-id': channel.id})
                await ctx.send(f"{channel.name} Has Been Added To The DataBase!")

        elif type == "remove":
            remove_query = Query()
            try:
                self.channel_whitelist.remove(remove_query['channel-name'].search(channel.name))
                await ctx.send(f"channel {channel.name} has been removed!")
            except:
                await ctx.send("Channel Not Found In Database")

    @commands.Cog.listener()
    async def on_message(self, message):

        if self.channel_whitelist.get(where('channel-id') != message.channel.id):
            pic_ext = ['.jpg', '.png', '.jpeg']
            if message.attachments != []:
                for ext in pic_ext:
                    attach = str(message.attachments[0])
                    if attach.endswith(f"{ext}\'>"):
                        dm_message = discord.Embed(title="Embed Detected!", color=0xff0000)
                        dm_message.add_field(name="Attention:",
                                             value=f"Our System has detected that you have sent a message containing an {ext} file, if you are a 3D artist,please use CHANNEL or show your work to USER!")
                        await message.author.send(embed=dm_message)


def setup(bot):
    bot.add_cog(EmbedDetection(bot))
