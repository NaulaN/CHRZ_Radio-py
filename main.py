import os

from discord import Intents,utils,ActivityType,Activity
from discord.ext import commands

from src.commands.help import Help
from src.commands.ping import PingCommand
from src.commands.set_radio import SetRadioCommand
from src.file_manager import FileManager
from src.radio import Radio


def set_permissions():
	perms = Intents.all()
	perms.presences = True
	perms.members = True
	perms.messages = True
	perms.guilds = True
	perms.guild_messages = True
	perms.reactions = True
	return perms


file_manager = FileManager()
config = file_manager.load('cfg.ini',f'{os.getcwd()}/res/')


class Bot(commands.Bot):

	def __init__(self):
		commands.Bot.__init__(self,command_prefix='.',intents=set_permissions(),help_command=None)

		self.version = config["BOT"]["version"]
		self.emoji_next_music = config["RADIO"]["emoji_next_music"]
		self.emoji_previous_music = config["RADIO"]["emoji_previous_music"]
		self.emoji_resume_music = config["RADIO"]["emoji_resume_music"]
		self.emoji_stop_music = config["RADIO"]["emoji_stop_music"]
		self.emoji_add_bot = config["RADIO"]["emoji_add_bot"]
		self.emoji_add_favorite = config["RADIO"]["emoji_add_favorite"]
		self.emoji_remove_bot = config["RADIO"]["emoji_remove_bot"]
		self.emoji_remove_favorite = config["RADIO"]["emoji_remove_favorite"]
		self.emoji_random_music = config["RADIO"]["emoji_random_music"]
		self.emoji_change_playlist = config["RADIO"]["emoji_change_playlist"]

		self.count = 0
		self.bot_id = 867406584316166145

		self.data = file_manager.load('guilds_data.json',f'{os.getcwd()}/res/')

		self.add_all_cogs()

	async def change_activity(self,name,status='dnd'):
		act = Activity(type=ActivityType.listening,name=name)
		await self.change_presence(activity=act,status=status)

	def add_all_cogs(self):
		for obj in [Radio(self),SetRadioCommand(self),PingCommand(self),Help(self)]:
			self.add_cog(obj)

	async def on_ready(self):
		print("[ ! Info ] Je suis prêt !\n=-----------------------=")

	async def on_raw_reaction_add(self,event):
		# Banner (Dirty Code)
		if event.message_id == 867436601712705536:
			guild = utils.get(self.guilds,id=event.guild_id)
			textChannel = utils.get(guild.channels,id=event.channel_id)
			message = textChannel.get_partial_message(event.message_id)
			await message.remove_reaction(event.emoji,event.member)


bot = Bot()
bot.run(config["BOT"]["TOKEN"])
