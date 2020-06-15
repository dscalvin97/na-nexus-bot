import discord
import asyncio

from discord.ext import commands

# manage extensions that contain commands, cogs and listeners used by the bot in runtime


class ExtensionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load an inactive extension
    @commands.command()
    async def LoadExtension(self, ctx, extName):
        await ctx.message.channel.send(f'`Loading Extension {extName}`')

        try:
            self.bot.load_extension(extName)
            return await ctx.message.channel.send(f'`{extName} loaded`')
        except Exception as e:
            return await ctx.message.channel.send(f'`Failed to load Extension {extName}\n{e}`')

    # Unload an active extension
    @commands.command()
    async def UnloadExtension(self, ctx, extName):
        await ctx.message.channel.send(f'`Unloading Extension {extName}`')

        try:
            extension = self.bot.extensions.index(extName)
            self.bot.unload_extension(extension)
            return await ctx.message.channel.send(f'`{extName} unloaded`')
        except Exception as e:
            return await ctx.message.channel.send(f'`Failed to unload Extension {extName}\n{e}`')

    # Reloads an extension
    @commands.command(aliases=['reload', 'reloadext', 'extreload'])
    async def ReloadExtension(self, ctx, extensionName):
        await ctx.message.channel.send(f'`Reloading Extension {extensionName}`')

        for extension in self.bot.extensions:
            if extension == extensionName:
                try:
                    self.bot.reload_extension(extension)
                    return await ctx.message.channel.send(f'`{extensionName} reloaded`')
                except Exception as e:
                    return await ctx.message.channel.send(f'`Failed to reload Extension {extensionName}\n{e}`')

    # Send list of active extensions in channel
    @commands.command(aliases=['extensions'])
    async def PrintExtList(self, ctx):
        separator = '\n'
        await ctx.channel.send(separator.join(self.bot.extensions))


def setup(bot):
    bot.add_cog(ExtensionManager(bot))
