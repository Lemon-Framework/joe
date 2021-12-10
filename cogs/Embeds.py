import discord
from discord.ext import commands

client = discord.Client()


class Embeds(commands.Cog):

	def __init__(self, client):
		self.client = client

	# cog has been successfully loaded
	@commands.Cog.listener()
	async def on_ready(self):
		print("Data commands - ✔️ ")

	@commands.command()
	@commands.has_permissions(manage_messages = True)
	async def embed(self, ctx, color, title, *arguments):
		color = int(color, 16)
		embed = discord.Embed(
			color = color,
			title = title.replace("~", " "),
			description = " ".join(arguments).replace("\\n", "\n")
		)
		await ctx.channel.purge(limit=1)
		await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(Embeds(client))