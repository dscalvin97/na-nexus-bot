import discord
import csv

from discord.ext import commands
from dateutil import rrule
from datetime import datetime, timedelta

# Cog to collect user message data for use in data visualization
class MessageDataCollector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # collects message data of the entire guild and saves it in a csv file.
    @commands.command()
    async def CollectData(self, ctx):
        await ctx.channel.send("`Iterating...`")
        async with ctx.channel.typing():
            command_start_time = datetime.now()
            guildcreationdate = ctx.guild.created_at
            enddate = datetime.utcnow()

            with open(f'{guildcreationdate.strftime("week%U.%b.%Y")}-{enddate.strftime("week%U.%b.%Y")}.csv', mode='w', newline='') as csv_file:
                csv_headers_list = ['message_id', 'message_timestamp']
                csv_writer = csv.DictWriter(csv_file, fieldnames=csv_headers_list)
                csv_writer.writeheader()

                #iterate through a week
                for week in rrule.rrule(freq=rrule.WEEKLY, dtstart=guildcreationdate, until=enddate):
                    time_range_end = week + timedelta(weeks=1)

                    for channel in ctx.guild.text_channels:
                        async for message in channel.history(before=time_range_end, after=week, oldest_first=True):
                            csv_writer.writerow({
                                'message_id': f'{message.id}',
                                'message_timestamp': f'{message.created_at.__str__()}'
                                })

            csv_file.close()

        total_time_operation  = datetime.now() - command_start_time
        await ctx.channel.send(f"`The operation took {total_time_operation .total_seconds()} seconds.`")

def setup(bot):
    bot.add_cog(MessageDataCollector(bot))

def teardown(bot):
    pass