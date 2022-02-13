import discord
from discord.ext import commands
import logging
import os
import helper

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=helper.Db.get_value("prefix"),intents=intents)

extensions = [
    file.split(".")[0] for file in os.listdir("./Cogs") if file.endswith(".py")
]

for file in extensions:
    client.load_extension("Cogs."+file)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

with open("token.txt","r") as f:
    token = f.readline()

client.run(token)