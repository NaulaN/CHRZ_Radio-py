from typing import Optional
from discord import Embed
from discord.ext import commands


class HelpCommand( commands.Cog ):

	def __init__(self, bot):
		self.bot = bot

		self.info_per_commands = {
			"ping": """
			**La commande** `.ping` **vous renvoie la latence du bot en millesecondes.**
			
			__Vous avez un petit indicator rapide__:
			🟢 Vous informe que le ping du bot est excellent.
			🟠 Vous informe que le ping du bot est correct.
			🔴 Vous informe que le ping du bot est null mais vraiment... Trés null.
			""",
			"set_radio": """
			**La commande** `.set_radio` **est destiné au propriétaire du serveur !**
			""",
			"help": """
			**La commande** `.help` **vous renvoie des details des commandes et la liste des commandes disponible.**
			""" }

	@commands.command(name= 'help')
	async def commands_list(self, ctx, commande: Optional[str]= None):
		if commande is None:
			return await ctx.send(embed= Embed(title= '> **Vous avez appelez** `.help` !', description= """
			__Les commandes disponible sont__:
				◽ .help
				◽ .ping
				◽ .set_radio
			
			_Pour plus d'info, entrez cette commande .help <commande>_""", color= 0xc0c0c0))
		return await ctx.send(embed= Embed(title= f'> **Vous avez appelez** `.help {commande}`', description= self.info_per_commands[commande], color= 0xc0c0c0))

