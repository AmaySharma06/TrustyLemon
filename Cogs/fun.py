from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f"Pong!\nLatency : `{round(self.client.latency*1000,3)}ms`")
        
def setup(client):
    client.add_cog(Fun(client))