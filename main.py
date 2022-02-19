import discord
from discord.ext import commands
import logging
import os
import Cogs.helper as helper
from keep_alive import keep_alive

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.members = True

def get_prefix(bot,message):
    return helper.Db.get_value("prefix")
client = commands.Bot(command_prefix=get_prefix,intents=intents)

extensions = [
    file.split(".")[0] for file in os.listdir("./Cogs") if file.endswith(".py") and file[:-3] not in ("helper","__init__")
]

for file in extensions:
    client.load_extension("Cogs."+file)

token = os.environ.get("token")
if not token:
    with open("token.txt","r") as f:
        token = f.readline()
        client.run(token)
      
keep_alive()
client.run(token)