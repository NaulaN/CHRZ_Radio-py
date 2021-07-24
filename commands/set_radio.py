from discord import Embed
from discord.ext import commands
from scripts import is_owner
import time, json


class SetRadioCommand( commands.Cog ):

	def __init__( self, bot ):
		self.bot = bot

		self.banner = "https://eapi.pcloud.com/getpubthumb?code=XZF400Z51SjOJbhU84OdCAe3k2ESVBtvE3X&linkpassword=undefined&size=1078x190&crop=0&type=auto"
		self.create_embed = lambda title, description, color: Embed( title= title, description= description, color= color )

	@commands.check( is_owner )
	@commands.command( name= 'set_radio' )
	async def set_radio( self, ctx ):
		# Message sending
		await ctx.send( content= self.banner )
		time.sleep( .5 )
		await ctx.send( embed= self.create_embed( "> 🎵 **𝘾𝙃𝙍𝙕 𝙍𝙖𝙙𝙞𝙤** 🎶, 𝘊𝘩𝘪𝘭𝘭 & 𝘓𝘰-𝘍𝘪", "🟢 -> Ajoute le bot à votre salon vocal\n🔴 -> Supprime le bot de votre salon vocal", color= 0xab11cc ) )

		self.bot.data[str(ctx.guild.id)]['message_radio_id'] = int( ctx.channel.last_message_id )
		self.bot.data[str(ctx.guild.id)]['channel_radio'] = int(ctx.channel.id)
		message = ctx.channel.get_partial_message( self.bot.data[str(ctx.guild.id)]['message_radio_id'] )

		# Reaction ( Radio button )
		await message.add_reaction(self.bot.emoji_add_bot)
		await message.add_reaction(self.bot.emoji_remove_bot)
		await message.add_reaction(self.bot.emoji_previous_music)
		await message.add_reaction(self.bot.emoji_stop_music)
		await message.add_reaction(self.bot.emoji_resume_music)
		await message.add_reaction(self.bot.emoji_next_music)

		with open( 'guilds_data.json', 'w' ) as f:
			json.dump( self.bot.data, f )
			f.close()
