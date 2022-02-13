from discord.ext import commands
import datetime 
import helper

class Events(commands.Cog):


    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        time = (datetime.datetime.utcnow() + datetime.timedelta(hours=5,minutes=30)).strftime("%H:%M:%S")
        print(f"Started at {time} as {client.user}")
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = helper.Db.get_value("welcome")
        channel = member.guild.get_channel(channel)

        await channel.send(f"<@{member.id}> joined")

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = helper.Db.get_value("leave")
        channel = member.guild.get_channel(channel)

        await channel.send(f"<@{member.id}> left")

def setup(client):
    client.add_cog(Events(client))

