from discord.ext import commands
from discord.utils import get
import helper

class Moderation(commands.Cog):

    def __init__(self,client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.manage_messages

    @commands.command()
    async def kick(self,ctx,member,reason=None):
        member = helper.check_member(ctx, member)
        await ctx.send(f"Kicked `{member.user}` from the server")
        await member.kick(reason=reason)
    
    @commands.command()
    async def ban(self,ctx,member,reason=None):
        member = helper.check_member(ctx, member)
        await ctx.send(f"Banned `{member.user}` from the server")
        await member.ban(reason=reason)
        
    @commands.command()
    async def mute(self,ctx,member):
        member = helper.check_member(ctx, member)
        mute_role = ctx.guild.get_role(helper.Db.get_value("mute"))
        await member.add_role(mute_role)
        await ctx.send(f"Muted `{member.user}`")
    
    @commands.command()
    async def unmute(self,ctx,member):
        member = helper.check_member(ctx, member)
        mute_role = ctx.guild.get_role(helper.Db.get_value("mute"))
        await member.remove_roles(mute_role)
        await ctx.send(f"Muted `{member.user}`")
    
    @commands.command()
    async def warn(self,ctx,member,*,reason):
        member = helper.check_member(ctx, member)
        helper.Db.warn_(member, reason)
        await ctx.send(f"Warned `{member.user}` for {reason}")
    
    @commands.command()
    async def clear(self,ctx,count):
        await ctx.channel.purge(limit=(count+1))
        await ctx.send(f"Purged {count} messages!",delete_after=5)

