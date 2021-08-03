from discord import utils
from file_manager import FileManager
import os


file_manager = FileManager()
ids = file_manager.load( 'guilds_data.json', f'{os.getcwd()}/res/' )

def doc_command_only_can_execute( ctx ):
	guild = utils.get( ctx.bot.guilds, id = ctx.message.guild.id )
	return ctx.channel.id in [ ids[ str( guild.id ) ][ 'id_channel_commandes' ], ids[ str( guild.id ) ][ 'id_channel_developers' ] ]


def is_owner( ctx ):
	guild = utils.get( ctx.bot.guilds, id = ctx.message.guild.id )
	return ctx.message.author.id == guild.owner_id


def python_command_only_can_execute( ctx ):
	guild = utils.get( ctx.bot.guilds, id = ctx.message.guild.id )
	try:
		condition = [ ids[ str( guild.id ) ][ 'id_channel_python' ], ids[ str( guild.id ) ][ 'id_channel_commandes' ], ids[ str( guild.id ) ][ 'id_channel_developers' ] ]
		return ctx.channel.id in condition
	except KeyError:
		return ctx.channel.id == ids[ str( guild.id ) ][ 'id_channel_commandes' ]
