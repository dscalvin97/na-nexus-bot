"""This extension provides cogs tailored to management of roles within a server"""
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
from tinydb import where
from tinydb.operations import add, subtract


# commands to get statistical data for roles
class RoleStatistics(commands.Cog):
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


# handles manual and self role assignment
class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_cache_setup()

    max_assignment_time = timedelta(seconds=20)

    async def CloseSetRole(self, member, message):
        roles_to_add = []
        for reaction in message.reactions:
            if reaction.count > 1:
                roles_to_add.append(
                    self.guild.get_role(
                        self.role_connections.get(where("emoji") == str(reaction))[
                            "role-id"
                        ]
                    )
                )

        tracked_roles_list = [
            self.guild.get_role(entry["role-id"]) for entry in self.role_connections
        ]

        new_roles_list = self.EditList("remove", member.roles, tracked_roles_list)
        await member.edit(roles=new_roles_list)
        new_roles_list = self.EditList("add", new_roles_list, roles_to_add)
        self.tracked_role_messages.remove(where("message-id") == message.id)
        await member.edit(roles=new_roles_list)
        await message.delete()
        await member.send(
            f'`You have successfully been assigned the roles {["@"+role.name for role in roles_to_add]}!`'
        )

        self.tracked_role_messages.remove(where("message-id") == message.id)

    def data_cache_setup(self):
        if self.bot.is_ready():
            self.tracked_role_messages = self.bot.db.table("rolemgr-tracked-messages")
            self.role_connections = self.bot.db.table("rolemgr-roles-connection")
            self.self_assignment_channel = self.bot.get_channel(
                self.bot.config["extension-data"]["rolemgr"]["role-setup-channel-id"]
            )

            if self.self_assignment_channel is None:
                self.self_assignment_channel = self.bot.get_guild(
                    self.bot.config["guild-id"]
                ).system_channel

            self.guild = self.bot.get_guild(self.bot.config["guild-id"])

    def EditList(self, argument, list1, list2):
        return {
            "add": list1 + list(set(list2) - set(list1)),
            "remove": list(set(list1) - set(list2)),
            "replace": list2,
        }[argument]

    @commands.command()
    async def SelfRoleStat(self, ctx):
        try:
            embed = discord.Embed(title="Self-role assignment stats", color=0x7289DA)

            embed.add_field(
                name="Self Assignment Channel",
                value=self.self_assignment_channel.name,
                inline=False,
            )
            embed.add_field(
                name="Role and emoji associations",
                value=[
                    f"{self.guild.get_role(entry['role-id']).mention}: {entry['emoji']}"
                    for entry in self.role_connections.all()
                ],
                inline=False,
            )
            embed.add_field(
                name="Active self role messages",
                value=len(self.tracked_role_messages.all()),
                inline=False,
            )

            await ctx.send(embed=embed)
        except AttributeError as e:
            print(e)

    # manually edit roles for members
    @commands.command()
    async def RoleEdit(self, ctx, edit_command, *mentions: discord.Role):
        roles_to_edit = ctx.message.role_mentions

        for member in mentions:
            try:
                new_roles_list = self.EditList(
                    edit_command, member.roles, roles_to_edit
                )
                await member.edit(roles=new_roles_list)
            except Exception as e:
                await ctx.send(
                    f"```Could not {edit_command} roles for user {member.name}\n{e}```"
                )

    # command to associate emoji reactions to roles for self assignment
    @commands.command()
    async def ConnectRole(self, ctx, emoji, role: discord.Role):
        if self.role_connections.get(
            (where("emoji") == emoji) & (where("role-id") != role.id)
        ):
            return await ctx.send(
                f"```The emoji {emoji} is already under use. Please use another emoji for this role.```"
            )
        self.role_connections.upsert(
            {"emoji": emoji, "role-id": role.id}, where("role-id") == role.id
        )
        await ctx.send(f"```associated @{role} to {emoji}```")

    @commands.command()
    async def SetRoleAssignChannel(self, ctx):
        self.self_assignment_channel = ctx.channel
        await ctx.send(
            f"```set #{ctx.channel.name} as the role self assignment channel```"
        )

    # start role self-assignment process, requires prior setup of emoji_for_roles
    @commands.command()
    @commands.cooldown(
        rate=1, per=max_assignment_time.total_seconds(), type=commands.BucketType.user
    )
    async def SetRole(self, ctx):
        if ctx.channel != self.self_assignment_channel:
            return

        role_msg_embed = discord.Embed(color=0x7289DA)

        embed_content = ""
        for entry in self.role_connections.all():
            embed_content += f'@{ctx.message.guild.get_role(entry["role-id"]).name}: {entry["emoji"]}\n'

        role_msg_embed.add_field(name="Domain Roles", value=embed_content)

        # send user message with embed
        tracked_message = await ctx.message.author.send(
            content=f"Hey {ctx.message.author.name}, please have a look below and choose your roles based on your field(s) of expertise.",
            embed=role_msg_embed,
        )

        self.tracked_role_messages.insert(
            {
                "user-id": ctx.message.author.id,
                "message-id": tracked_message.id,
                "count": 0,
                "timestamp": datetime.utcnow().__str__(),
            }
        )

        # set reactions for message
        for entry in self.role_connections.all():
            await tracked_message.add_reaction(entry["emoji"])

    @commands.Cog.listener()
    async def on_ready(self):
        self.data_cache_setup()
        self.tracked_message_delete.start()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # update count on actively tracked message reactions
        if not user.bot:
            self.tracked_role_messages.update(
                add("count", 1), where("message-id") == reaction.message.id
            )

            member = self.guild.get_member(user.id)

            if (
                self.tracked_role_messages.get(
                    where("message-id") == reaction.message.id
                )["count"]
                == 3
            ):
                await self.CloseSetRole(member=member, message=reaction.message)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        # update count on actively tracked message reactions
        if not user.bot:
            self.tracked_role_messages.update(
                subtract("count", 1), where("message-id") == reaction.message.id
            )

    @tasks.loop(seconds=1)
    async def tracked_message_delete(self):
        for entry in self.tracked_role_messages:
            message_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
            if datetime.utcnow() - message_time > self.max_assignment_time:
                member = self.guild.get_member(entry["user-id"])
                message = await member.fetch_message(entry["message-id"])
                await self.CloseSetRole(member=member, message=message)
                self.tracked_role_messages.remove(
                    where("message-id") == entry["message-id"]
                )


def last_cmd_call(ctx):
    return True


def setup(bot):
    bot.add_cog(RoleStatistics(bot))
    bot.add_cog(RoleManagement(bot))


def teardown(bot):
    pass
