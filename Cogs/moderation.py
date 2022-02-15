from discord.ext import commands
from discord.utils import get
import discord
from . import helper

class Moderation(commands.Cog):

    def __init__(self,client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.manage_messages

    @commands.command()
    async def kick(self,ctx,member:discord.Member,reason=None):
        await ctx.send(f"Kicked `{member}` from the server")
        await member.kick(reason=reason)
    
    @commands.command()
    async def ban(self,ctx,member:discord.Member,reason=None):
        await ctx.send(f"Banned `{member}` from the server")
        await member.ban(reason=reason)
        
    @commands.command()
    async def mute(self,ctx,member:discord.Member):
        mute_role = ctx.guild.get_role(helper.Db.get_value("mute"))
        await member.add_roles(mute_role)
        await ctx.send(f"Muted `{member}`")
    
    @commands.command()
    async def unmute(self,ctx,member:discord.Member):
        mute_role = ctx.guild.get_role(helper.Db.get_value("mute"))
        await member.remove_roles(mute_role)
        await ctx.send(f"Umuted `{member}`")
    
    @commands.command()
    async def warn(self,ctx,member:discord.Member,*,reason):
        helper.Db.warn_(member, reason)
        await ctx.send(f"Warned `{member}` for {reason}")
    
    @commands.command()
    async def clear(self,ctx,count:int):
        await ctx.channel.purge(limit=(count+1))
        await ctx.send(f"Purged {count} messages!",delete_after=2.5)

def setup(client):
    client.add_cog(Moderation(client))
