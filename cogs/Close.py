import discord
from discord.ext import commands

client = discord.Client()


class Close(commands.Cog):

	def __init__(self, client):
		self.client = client

	# cog has been successfully loaded
	@commands.Cog.listener()
	async def on_ready(self):
		print("Close commands - ✔️ ")

	@commands.command()
	async def close(self, ctx):
		if not ctx.channel.name.startswith("ticket"):
			return

		await ctx.channel.edit(category = ctx.guild.categories[4], overwrites = {
			ctx.guild.default_role:
     discord.PermissionOverwrite(read_messages=False),
			ctx.author: discord.PermissionOverwrite(read_messages=False, send_messages=False)
		})

		


def setup(client):
    client.add_cog(Close(client))