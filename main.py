from discord import Intents, utils, ActivityType, Activity, Status
from discord.ext import commands

from commands.help import HelpCommand
from commands.ping import PingCommand
from commands.set_radio import SetRadioCommand
from radio import Radio

import configparser, json, os


i = Intents.all()
i.presences = True
i.members = True
i.messages = True
i.guilds = True
i.guild_messages = True
i.reactions = True

config = configparser.ConfigParser()
config.read( 'res/cfg.ini', encoding= 'UTF-8' )


class Bot(commands.Bot):

	def __init__(self):
		help_command = HelpCommand(self)
		commands.Bot.__init__(self, command_prefix= '.', intents= i, help_command= help_command.commands_list)

		self.version = config["BOT"]["version"]

		self.emoji_next_music = config["RADIO"]["emoji_next_music"]
		self.emoji_previous_music = config["RADIO"]["emoji_previous_music"]
		self.emoji_resume_music = config["RADIO"]["emoji_resume_music"]
		self.emoji_stop_music = config["RADIO"]["emoji_stop_music"]
		self.emoji_add_bot = config["RADIO"]["emoji_add_bot"]
		self.emoji_remove_bot = config["RADIO"]["emoji_remove_bot"]
		self.emoji_random_music = config["RADIO"]["emoji_random_music"]

		self.count = 0
		self.bot_id = 867406584316166145

		__path = os.path.join( f'{os.getcwd()}/res/', 'guilds_data.json' )
		with open(__path) as f:
			self.data = json.load(f)
			f.close()

	async def change_activity(self, name, status):
		act = Activity(type= ActivityType.listening, name= name, status= status)
		await self.change_presence(activity= act)

	async def on_ready(self):
		print("Je me lance, veuillez patientez...")

		radio = Radio(self)
		set_radio_command = SetRadioCommand(self)
		ping_command = PingCommand(self)

		self.add_cog(radio)
		self.add_cog(set_radio_command)
		self.add_cog(ping_command)

		await self.change_activity(f"Musics 𝘊𝘩𝘪𝘭𝘭 & 𝘓𝘰-𝘍𝘪 | {self.version}", Status.do_not_disturb)

		print("[ ! Info ] Je suis prêt !\n=-----------------------=")

	async def on_message(self, message):
		await self.process_commands( message )

	async def on_raw_reaction_add(self, event):
		# Banner
		if event.message_id == 867436601712705536:
			guild = utils.get(self.guilds, id= event.guild_id)
			textChannel = utils.get(guild.channels, id= event.channel_id)
			message = textChannel.get_partial_message(event.message_id)
			await message.remove_reaction(event.emoji, event.member)


bot = Bot()
bot.run(config["BOT"]["TOKEN"])
