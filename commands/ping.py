from discord import Embed
from discord.ext import commands


class PingCommand( commands.Cog ):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name= 'ping')
	async def ping_request(self, ctx):
		bot_latency = round(self.bot.latency * 1000)
		indicator = "⚪"

		if bot_latency <= 100.0:
			indicator = "🟢"
		elif 100.0 <= bot_latency <= 200.0:
			indicator = "🟠"
		elif bot_latency >= 200.0:
			indicator = "🔴"

		await ctx.send( embed= Embed( title= "> **Ping Request**", description= f"{indicator} __latency:__ **{bot_latency}**", color= 0xc0c0c0 ) )
