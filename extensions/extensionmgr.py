import discord
import asyncio

from discord.ext import commands


# manage extensions that contain commands, cogs and listeners used by the bot in runtime
class ExtensionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_extension_reloaded = ''

    # loads an extension
    @commands.command()
    async def LoadExtension(self, ctx, extension_name):
        await ctx.message.channel.send(f'`Loading Extension {extension_name}`')

        try:
            self.bot.load_extension(extension_name)
            return await ctx.message.channel.send(f'`{extension_name} loaded`')
        except Exception as e:
            return await ctx.message.channel.send(f'`Failed to load Extension {extension_name}\n{e}`')

    # unloads an extension
    @commands.command()
    async def UnloadExtension(self, ctx, extension_name):
        await ctx.message.channel.send(f'`Unloading Extension {extension_name}`')

        try:
            self.bot.unload_extension(extension_name)
            return await ctx.message.channel.send(f'`{extension_name} unloaded`')
        except Exception as e:
            return await ctx.message.channel.send(f'`Failed to unload Extension {extension_name}\n{e}`')

    # reloads an extension
    @commands.command(aliases=['reload', 'reloadext', 'extreload'])
    async def ReloadExtension(self, ctx, extension_name=''):
        await ctx.message.channel.send(f'`Reloading Extension {extension_name}`')

        if extension_name == '':
            if self.last_extension_reloaded != '':
                extension_name = self.last_extension_reloaded
            else:
                return await ctx.send('Please mention the extension name as no extension has been reloaded previously in this instance.')

        try:
            self.bot.reload_extension(extension_name)
            self.last_extension_reloaded = extension_name
            return await ctx.send(f'`{extension_name} reloaded`')
        except Exception as e:
            return await ctx.send(f'`Failed to reload Extension {extension_name}\n{e}`')

    # send list of active extensions in channel
    @commands.command(aliases=['extensions'])
    async def PrintExtList(self, ctx):
        separator = '\n'
        await ctx.channel.send(f'`{separator.join(self.bot.extensions)}`')


def setup(bot):
    bot.add_cog(ExtensionManager(bot))
