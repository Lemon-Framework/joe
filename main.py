import discord
import os
from keep_alive import keep_alive
import re
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents().default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix="$", intents=intents)
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
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="Lemon on GitHub"))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        matches = []
        for command in client.commands:
            if (
                    re.findall(f"[{ctx.message.content[1:]}]+", command.name)
            ):  # i know, bad way to do it but it kinda works and its simple
                matches.append(command.name)
        similar = ""
        if matches:
            similar = "Similar commands: " + ", ".join(matches)
        await ctx.channel.send(content=f"Command not found!\n{similar}")
    else:
        print(error)


for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

roles = {"🐱": "github", "🎉": "announcements", "📢": "events"}


@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 918887016832331828:
        if payload.emoji.name in roles:
            guild = client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles,
                                     name=roles[payload.emoji.name])
            await payload.member.add_roles(role)

    if payload.channel_id == 1002247733362573402:
        if payload.emoji.name == "🎫":
            f = open("tickets", "r+")
            tickets = int(f.read()) + 1
            f.seek(0)
            f.write(str(tickets))
            f.close()
            guild = client.get_guild(payload.guild_id)
            channel = await guild.categories[1].create_text_channel(
                f"ticket-{tickets}",
                overwrites={
                    guild.default_role:
                    discord.PermissionOverwrite(read_messages=False),
                    payload.member:
                    discord.PermissionOverwrite(read_messages=True,
                                                send_messages=True)
                })
            await channel.send(
                f"{payload.member.mention} please describe the problem here.")


@client.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == 918887016832331828:
        if payload.emoji.name in roles:
            guild = client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles,
                                     name=roles[payload.emoji.name])
            await guild.get_member(payload.user_id).remove_roles(role)


@client.event
async def on_member_join(member):
    await member.add_roles(
        discord.utils.get(member.guild.roles, name="\Lemon\Discord\Member"))


keep_alive()
client.run(TOKEN)
