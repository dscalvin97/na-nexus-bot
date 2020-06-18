import discord
import asyncio

from discord.ext import commands
from typing import List


class MessageManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # message check for DeleteMessages command
    def purge_check(self, message):
        member_check = True

        if len(self.check_data['users']) > 0:
            member_check = message.author in self.check_data['users']

        return (self.check_data['target_content'] in message.content) and (not message.id in [msg.id for msg in self.check_data['del_msgs']]) and (member_check)

    # delete messages which contain the target content, or are by sent by specific users, or both
    @commands.command(aliases=['delmsgs'])
    @commands.has_permissions(manage_messages=True)
    async def DeleteMessages(self, ctx, target_content='', msglimit=200, *users: discord.User):
        separator = ', '
        delete_msgs_after_command = []
        self.check_data = {}

        user_names = [user.name for user in users]
        start_message = await ctx.message.channel.send(f'`Looking for messages that contain "{target_content}" by {separator.join(user_names)} in the last {msglimit} messages`')

        delete_msgs_after_command.append(ctx.message)
        delete_msgs_after_command.append(start_message)

        self.check_data['users'] = users
        self.check_data['target_content'] = target_content
        self.check_data['del_msgs'] = delete_msgs_after_command

        deleted_msgs = await ctx.message.channel.purge(limit=msglimit+2, check=self.purge_check)

        end_message = await ctx.message.channel.send(f'`{len(deleted_msgs)} out of {msglimit} messages have been deleted`\n`The command and bot messages will be deleted in 10 seconds from now`')
        delete_msgs_after_command.append(end_message)

        await asyncio.sleep(10)

        try:
            await ctx.message.channel.purge(limit=len(delete_msgs_after_command))
        except Exception as e:
            return await ctx.message.channel.send(f'`{e}`')


def setup(bot):
    bot.add_cog(MessageManager(bot))


def teardown(bot):
    pass
