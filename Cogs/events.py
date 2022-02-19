from discord.ext import commands
import datetime 
from . import helper


class Events(commands.Cog):


    def __init__(self,client):
        self.client = client
        self.censors = helper.Db.get_value("censor")


    @commands.Cog.listener()
    async def on_ready(self):
        time = (datetime.datetime.utcnow() + datetime.timedelta(hours=5,minutes=30)).strftime("%H:%M:%S")
        print(f"Started at {time} as {self.client.user}")
    
    # @commands.Cog.listener()
    # async def on_member_join(self,member):
    #     channel = helper.Db.get_value("welcome")
    #     channel = member.guild.get_channel(channel)

    #     await channel.send(f"<@{member.id}> joined")

    # @commands.Cog.listener()
    # async def on_member_remove(self,member):
    #     channel = helper.Db.get_value("leave")
    #     channel = member.guild.get_channel(channel)

    #     await channel.send(f"<@{member.id}> left")

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.id == 681770687614156811 and message.channel.id == 829651225212354570 and "Achievement" in message.content:
            await self.react(message)
        for word in self.censors:
            if word in message.content.lower() and message.author!=self.client.user and self.client.get_guild(740200656606068766).get_role(helper.Db.get_value("admin")) not in message.author.roles:
                await message.delete()

    async def react(self,message):
        emojis = [self.client.get_emoji(i) for i in [834504209108828211, 858720301692616745, 760066591948800050, 851114544013246474, 858694717210755104]]
        for i in emojis:
            await message.add_reaction(i)
    
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     msg = await ctx.send(f"Uh oh, something went wrong\n\n {str(error)}")
    #     me = self.client.get_user(860888011164483624)
    #     await me.send(str(error)+f"\n\n{msg.jump_url}")

def setup(client):
    client.add_cog(Events(client))

