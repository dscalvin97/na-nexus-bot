import discord
import json

from discord.ext import commands

# Provides Hot-Configurable User Authentication
class AuthConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ViewPerms(self, ctx):
        """View Permission Json"""
        await ctx.send(f'```{json.dumps(ctx.bot.auth)}```')
    
    @commands.command()
    async def LoadPerms(self, ctx):
        """Load Permissions"""
        ctx.bot.load_auth()
        await ctx.send('Loaded Permissions from File')
    
    @commands.command()
    async def SavePerms(self, ctx):
        """Save Permissions"""
        ctx.bot.save_auth()
        await ctx.send('Saved Permissions to File')
    
    @commands.command()
    async def SetWhitelist(self, ctx, member: discord.Member, *roles: discord.Role):
        """Set whitelisted roles for Member

        Args:
            member: Member to set whitelist roles.
            roles: Roles to whitelist.
        """
        whitelist = ctx.bot.auth['whitelist']
        whitelist[str(member.id)] = [role.id for role in roles]
        
        await ctx.send(f'Set whitelists for {member.display_name}.')
    
    @commands.command()
    async def SetCommandPerms(self, ctx, command_name: str, *roles: discord.Role):
        """Set roles which can run a command

        Args:
            command: Command to set permissions for.
            roles: Roles to grant permission. If you specify none, any member can run the command.
        """
        command = ctx.bot.get_command(command_name)
        if command:
            permissions = ctx.bot.auth['permissions']
            permissions[command.cog_name][command.name] = [role.id for role in roles]
            
            await ctx.send(f'Set permissions for command {command.name}.')
        else:
            await ctx.send(f'No such command {command_name}.')
    
    @commands.command()
    async def SetCogPerms(self, ctx, cog_name: str, *roles: discord.Role):
        """Set roles which can by default run commands for a cog

        Args:
            cog: Cog to set permissions for.
            roles: Roles to grant permission. If you specify none, any member can run the command.
        """
        cog = ctx.bot.get_cog(cog_name)
        if cog:
            permissions = ctx.bot.auth['permissions']
            permissions[cog.name]['__default__'] = [role.id for role in roles]
            
            await ctx.send(f'Set permissions for cog {cog.name}.')
        else:
            await ctx.send(f'No such cog {cog_name}.')
    
def setup(bot):
    bot.add_cog(AuthConfig(bot))

def teardown(bot):
    pass