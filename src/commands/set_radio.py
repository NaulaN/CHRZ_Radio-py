import os
import time
import json

from discord import Embed
from discord.ext import commands

from scripts import is_owner


class SetRadioCommand(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		self.banner = "https://eapi.pcloud.com/getpubthumb?code=XZF400Z51SjOJbhU84OdCAe3k2ESVBtvE3X&linkpassword=undefined&size=1078x190&crop=0&type=auto"
		self.create_embed = lambda title,description,illustrator,color: Embed(title=title,description=description,color=color).set_image(url=illustrator)

	@commands.check(is_owner)
	@commands.command(name='set_radio',alias=["sr"])
	async def set_radio(self,ctx):
		# Message sending
		await ctx.send(content=self.banner)
		time.sleep(.5)
		await ctx.send(embed=self.create_embed("> 🎵 **𝘾𝙃𝙍𝙕 𝙍𝙖𝙙𝙞𝙤** 🎶, 𝘊𝘩𝘪𝘭𝘭 & 𝘓𝘰-𝘍𝘪","🟢 -> Ajoute le bot à votre salon vocal\n🔴 -> Supprime le bot de votre salon vocal","https://thumbs.gfycat.com/WatchfulOpenGentoopenguin-size_restricted.gif",color=0xab11cc))

		self.bot.data[str(ctx.guild.id)]["message_radio_id"] = int(ctx.channel.last_message_id)
		self.bot.data[str(ctx.guild.id)]["channel_radio"] = int(ctx.channel.id)
		message = ctx.channel.get_partial_message(self.bot.data[str(ctx.guild.id)]['message_radio_id'])
		# Reaction (Radio button)
		for reaction in [self.bot.emoji_add_bot,self.bot.emoji_remove_bot,self.bot.emoji_previous_music,self.bot.emoji_stop_music,self.bot.emoji_resume_music,self.bot.emoji_next_music,self.bot.emoji_random_music,self.bot.emoji_add_favorite,self.bot.emoji_remove_favorite,self.bot.emoji_change_playlist]:
			await message.add_reaction(reaction)

		path = os.path.join(f"{os.getcwd()}/res/","guilds_data.json")
		with open(path,"w") as f:
			json.dump(self.bot.data,f)
			f.close()
