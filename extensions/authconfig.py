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
            member: Member to set whitelist roles
            roles: Roles to whitelist
        """
        whitelist = ctx.bot.auth['whitelist']
        for role in roles:
            whitelist[str(member.id)] = [role.id for role in roles]
        
        await ctx.send(f'Set whitelists for {member.display_name}.')
    
def setup(bot):
    bot.add_cog(AuthConfig(bot))

def teardown(bot):
    pass