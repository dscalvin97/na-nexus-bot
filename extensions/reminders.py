import discord
from tinydb import TinyDB, where
from datetime import datetime
import dateparser

from discord.ext import commands, tasks


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = bot.db.table('reminders')
        self.check_reminders.start()

    @tasks.loop(seconds=1.0)
    async def check_reminders(self):
        now = datetime.now().timestamp()
        for reminder in self.reminders.search(where('time') < now):
            self.reminders.remove(doc_ids=[reminder.doc_id])
            user = self.bot.get_user(reminder['user'])

            # construct embed
            embed = discord.Embed(
                title="Reminders", description=reminder['message'])
            embed.set_author(name=user.name, icon_url=user.avatar_url)

            # send reminders
            await user.send(embed=embed)
            for channel_id in reminder['channels']:
                channel = self.bot.get_channel(channel_id)
                await channel.send(embed=embed)

    @ check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()

    @ commands.command(aliases=['Remind'])
    async def Reminder(self, ctx, time: str, message: str, *channels: discord.TextChannel):
        time = dateparser.parse(time, settings={'PREFER_DATES_FROM': 'future'})
        if time:
            reminder_id = self.reminders.insert(
                {'message': message, 'time': time.timestamp(), 'channels': [channel.id for channel in channels], 'user': ctx.message.author.id})
            return await ctx.send(f'Added reminder with id {reminder_id} for {time}')
        else:
            return await ctx.send(f'Couldn\'t parse the specified time.')

    @ commands.command(aliases=['CancelReminder'])
    async def CancelReminders(self, ctx, *ids: int):
        self.reminders.remove(doc_ids=ids)
        return await ctx.send(f'Removed reminders.')


def setup(bot):
    bot.add_cog(Reminders(bot))
