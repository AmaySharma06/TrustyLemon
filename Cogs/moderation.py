from discord.ext import commands
from discord.utils import get
import discord
from . import helper


client_ = None


class Moderation(commands.Cog):

    def __init__(self,client):
        self.client = client
        global client_
        client_ = client
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
    async def clw(self,ctx,member:discord.Member,timestamp=None):
        helper.Db.unwarn_(member,timestamp)
        await ctx.send(f"Cleared warning with id `{timestamp}` for `{member}`")
    
    @commands.command(aliases=["warnings",])
    async def warns(self,ctx,member:discord.Member):
        for id,fields in helper.Db.get_value("warns").items():
            if id == str(member.id):
                field = fields
                break
        else: await ctx.send("Member has no warnings issued ||yet||"); return

        warnings = fields["warnings"]
        timestamps = fields["timestamps"]

        strings = ""
        for i in range(len(warnings)):
            strings += f"`{i+1}`. `{timestamps[i]}` : {warnings[i]}"
        
        embed = discord.Embed(
            title = f"Warnings for {member}", 
            colour = discord.Color.red(),
            description = strings
        )
        embed.set_footer(text="To remove a warning, use clw `mention` `timestamp`")

        await ctx.send(embed=embed) 

    @commands.command()
    async def clear(self,ctx,count:int):
        await ctx.channel.purge(limit=(count+1))
        await ctx.send(f"Purged {count} messages!",delete_after=2.5)
    
    @commands.group()
    async def censor(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid Command Passed")
    
    @censor.command()
    async def add(self,ctx,word:str):
        word = word.lower()
        censors = helper.Db.get_value("censor")
        if word not in censors:
            censors.append(word)
            helper.Db.set_value("censor", censors)
            await ctx.send(f"Added {word} to censor list!")
        else:
            await ctx.send("Censor already exists!")
        self.client.get_cog("Events").censors = helper.Db.get_value("censor")

    @censor.command()
    async def remove(self,ctx,word:str):
        word = word.lower()
        censors = helper.Db.get_value("censor")
        if word in censors:
            censors.remove(word)
            helper.Db.set_value("censor", censors)
            await ctx.send(f"Removed {word} from censor list!")
        else:
            await ctx.send("Censor does not exist!")    
        self.client.get_cog("Events").censors = helper.Db.get_value("censor")

    @commands.command()
    async def setprefix(self,ctx,prefix):
        helper.Db.set_value("prefix", prefix)

def setup(client):
    client.add_cog(Moderation(client))
