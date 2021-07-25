from discord import FFmpegPCMAudio, utils
from discord.ext import commands
from discord.ext.tasks import loop

import os, random


class Radio(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

		self.template = {"choice_musique": 0, "joined": False, "paused": False, "resume": True, "stopped": False, "random": False}
		self.all_voices = {}
		self.all_musics = os.listdir(f'{os.getcwd()}/Music')

		self.n = 0

	@staticmethod
	def play_music(music, voice):
		voice.stop() if voice.is_playing() else None
		sources = FFmpegPCMAudio(f'{os.getcwd()}/Music/{music}')
		return voice.play(sources)

	def start_loop(self):
		if not self.change_musique_loop.is_running():
			return self.change_musique_loop.start()

	def cancel_loop(self):
		if not self.change_musique_loop.is_being_cancelled():
			return self.change_musique_loop.stop()

	def change_music(self, op: str):
		self.all_voices[self.vocalChannel.id]["choice_musique"] += 1 if op == '+' else -1
		if (self.all_voices[self.vocalChannel.id]["choice_musique"] >= len(self.all_musics)-1) if op == '+' else (self.all_voices[self.vocalChannel.id]["choice_musique"] <= -1):
			self.all_voices[self.vocalChannel.id]["choice_musique"] = 0 if op == '+' else len(self.all_musics)-1

	async def leave(self, event, guild):
		# The bot leave the vocal channel
		if str(event.emoji) == self.bot.emoji_remove_bot:
			# leave vocal
			await guild.voice_client.disconnect()
			self.all_voices[self.vocalChannel.id]["joined"] = False
			self.cancel_loop()

	async def join(self, event, message):
		for member in self.vocalChannel.members:
			if self.bot.bot_id == member.id:
				await message.remove_reaction(event.emoji, event.member); return
		# join vocal
		self.voice = await self.vocalChannel.connect()
		self.all_voices[self.vocalChannel.id]["joined"] = True
		# set random value for first start of musique
		random_choice = random.randint(0, len(self.all_musics) - 1)
		self.all_voices[self.vocalChannel.id]["choice_musique"] = random_choice
		self.play_music(self.all_musics[random_choice], self.voice)
		await self.bot.change_activity(f"musics 𝘊𝘩𝘪𝘭𝘭 & 𝘓𝘰-𝘍𝘪 | {self.bot.version}", 'online')
		self.start_loop()

	async def next_music(self, event):
		if str(event.emoji) == self.bot.emoji_next_music and (self.voice.is_playing()):
			if self.all_voices[self.vocalChannel.id]["random"] is False:
				self.change_music('+')
			else:
				self.all_voices[self.vocalChannel.id]["choice_musique"] = random.randint(0, len(self.all_musics) - 1)
			self.play_music(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]], self.voice)

	async def back_music(self, event):
		if str(event.emoji) == self.bot.emoji_previous_music and (self.voice.is_playing()):
			self.change_music('-')
			self.play_music(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]], self.voice)

	async def stop_music(self, event):
		if (str(event.emoji) == self.bot.emoji_stop_music) and (self.voice.is_playing()):
			self.voice.stop()
			self.cancel_loop()

	async def resume_music(self, event):
		# Restart the music where is been stopped
		if (str(event.emoji) == self.bot.emoji_resume_music) and (not self.voice.is_playing()):
			self.play_music(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]], self.voice)
			self.start_loop()

	async def set_random_music_selection(self, event):
		# Set random selection of music
		if str(event.emoji) == self.bot.emoji_random_music:
			self.all_voices[self.vocalChannel.id]["random"] = True

	async def remove_random_music_selection(self, event):
		# Random selection of music
		if (str(event.emoji) == self.bot.emoji_random_music) and (event.member is not None):
			self.all_voices[self.vocalChannel.id]["random"] = False

	@commands.Cog.listener()
	async def on_ready(self):
		await self.change_activity_music.start()

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, event):
		if event.message_id == self.bot.data[str(event.guild_id)]['message_radio_id']:
			guild = utils.get(self.bot.guilds, id= event.guild_id)
			textChannel = utils.get(guild.channels, id= event.channel_id)
			self.vocalChannel = utils.get(guild.voice_channels, id= event.member.voice.channel.id)
			message = textChannel.get_partial_message(event.message_id)
			self.all_voices[self.vocalChannel.id] = self.template

			# The bot join the vocal channel where is the user
			await self.join(event, message) if str(event.emoji) == self.bot.emoji_add_bot else None
			# If joined a vocal channel
			if self.all_voices[self.vocalChannel.id]["joined"]:
				await self.leave(event, guild)
				await self.next_music(event)
				await self.back_music(event)
				await self.stop_music(event)
				await self.resume_music(event)
				await self.set_random_music_selection(event)
			# Remove after an action on reaction below of radio message
			await message.remove_reaction(event.emoji, event.member) if str(event.emoji) not in [self.bot.emoji_random_music] else None

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, event):
		# Radio message
		await self.remove_random_music_selection(event) if event.message_id == self.bot.data[str(event.guild_id)]['message_radio_id'] else None

	@loop(seconds= 3)
	async def change_musique_loop(self):
		await self.bot.wait_until_ready()

		self.all_voices[self.vocalChannel.id]["stopped"] = self.voice.is_paused()
		self.all_voices[self.vocalChannel.id]["resume"] = self.voice.is_playing()

		# Changing automatically the music if the previous music is finished
		if self.voice.is_playing() is False:
			if self.all_voices[self.vocalChannel.id]["random"] is False:
				self.change_music('+')
			else:
				self.all_voices[self.vocalChannel.id]["choice_musique"] = random.randint(0, len(self.all_musics) - 1)
			self.sources = FFmpegPCMAudio(f'./Music/{self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]]}')
			self.voice.play(self.sources)

	@loop(minutes= 1)
	async def change_activity_music(self):
		await self.bot.wait_until_ready()
		try:
			if self.all_voices[self.vocalChannel.id]["joined"]:
				name_act = [f"musics 𝘊𝘩𝘪𝘭𝘭 & 𝘓𝘰-𝘍𝘪 | {self.bot.version}", str(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]]).removesuffix('.mp3')]
				if self.n >= 2:
					self.n = 0
				await self.bot.change_activity(name_act[self.n], 'online')
				self.n += 1
		except AttributeError:
			await self.bot.change_activity(f"nothing | {self.bot.version}")

	@loop(minutes= 1)
	async def check_inactive(self):
		await self.bot.wait_until_ready()
		for guild in self.bot.guilds:
			member = utils.get(guild.members, id= self.bot.bot_id)

			if member.voice is not None:
				if (self.count >= 3) or (self.voice.is_playing() is False):
					self.count = 0
				await guild.voice_client.disconnect() if (len(member.voice.channel.members) == 1) and (self.count == 2) else None
				self.count += 1
