import discord
from discord import Embed
from discord.ext import commands


class PingCommand( commands.Cog ):

	def __init__(self, bot):
		self.bot = bot
		self.get_latency = lambda: round(self.bot.latency * 1000)

	@staticmethod
	def ping_indicator(latency):
		if latency <= 100.0:
			indicator = "🟢"
		elif 100.0 <= latency <= 200.0:
			indicator = "🟠"
		elif latency >= 200.0:
			indicator = "🔴"
		return indicator

	@commands.command(name= 'ping')
	async def ping_request(self, ctx):
		bot_latency = self.get_latency()
		indicator = self.ping_indicator(bot_latency)

		await ctx.send(embed= Embed(title= "> **Ping Request**", description= f"{indicator} __latency:__ **{bot_latency}**", color= 0xc0c0c0))
