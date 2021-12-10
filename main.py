import discord
import os
from keep_alive import keep_alive
import re
from discord.ext import commands
from dotenv import load_dotenv


intents = discord.Intents().default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix = "$", intents=intents)
client.remove_command("help")
load_dotenv()
TOKEN = os.getenv('TOKEN')

@client.event  
async def on_ready():
    print("-------------------------")
    print("Bot Name: " + client.user.name)
    print(client.user.id)
    print("API Version: " + discord.__version__)
    for guild in client.guilds:
        print(guild.name)

    print(client.latency * 1000)
    print("-------------------------")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Lemon on GitHub"))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        matches = []
        for command in client.commands:
            if (re.findall(f"[{ctx.message.content[1:]}]+", command.name)): # i know
                matches.append(command.name)
        similar = ""
        if matches:
            similar = "Similar commands: "+", ".join(matches)
        await ctx.channel.send(content=f"Command not found!\n{similar}")
    else:
        print(error)
        
for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
client.run(TOKEN)