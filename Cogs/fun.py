from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f"Pong!\nLatency : `{round(client.latency,3)}ms`")
        