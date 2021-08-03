from typing import Optional
from discord import Embed
from discord.ext import commands


class Help( commands.Cog ):

	def __init__(self, bot):
		self.bot = bot
		self.info_per_commands = {"ping": """
					**La commande** `.ping` **vous renvoie la latence du bot en millesecondes.**

					__Vous avez un petit indicator rapide__:
					🟢 Vous informe que le ping du bot est excellent.
					🟠 Vous informe que le ping du bot est correct.
					🔴 Vous informe que le ping du bot est null mais vraiment... Trés null.
					""", "set_radio": """
					**La commande** `.set_radio` **est destiné au propriétaire du serveur !**
					""", "help": """
					**La commande** `.help` **vous renvoie des details des commandes et la liste des commandes disponible.**
					"""}

	@commands.command(name= 'help')
	async def commands_list(self, ctx, commande: Optional[str]= None):
		if commande is None:
			return await ctx.send(embed=Embed(title='> **Vous avez appelé** `.help` !', description= f"""
			__Les commandes disponibles sont__:
				:white_small_square: .help
				:white_small_square: .ping
				:white_small_square: .set_radio
				
			__Info sur le channel Musique et des messages interne__:
				:white_small_square: {self.bot.emoji_add_bot} Permets d'ajouter la bot music à votre vocal channel
				:white_small_square: {self.bot.emoji_remove_bot} Permets de supprimer la bot music de votre vocal channel
				:white_small_square: {self.bot.emoji_next_music} Permets de changer de musique
				:white_small_square: {self.bot.emoji_previous_music} Permets de mettre la musique précédente
				:white_small_square: {self.bot.emoji_random_music} Permets une lecture aléatoire des musiques
				:white_small_square: {self.bot.emoji_resume_music} Permets de relance la lecture si la musique a été stoppée
				:white_small_square: {self.bot.emoji_stop_music} Permets d'arrêter la lecture

			_Pour plus d'infos, entrez cette commande .help <commande>_""", color=0xc0c0c0))
		return await ctx.send(embed=Embed(title=f'> **Vous avez appelez** `.help {commande}`', description= self.info_per_commands[commande], color=0xc0c0c0))

