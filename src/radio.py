import json
import os
import random

from discord import FFmpegPCMAudio,utils,Embed
from discord.ext import commands
from discord.ext.tasks import loop


class Radio(commands.Cog):
	all_voices: dict = {}
	all_playlist: list = os.listdir(f"{os.getcwd()}/res/Musics/")
	template: dict = {"creator": None,"choice_musique": 0,"joined": False,"paused": False,"resume": True,"stopped": False,"random": False}
	template_favorites_musics = {"musics": []}
	choice_random_musics: list = []
	switch_playlist: int = 0
	count: int = 0
	delete_after: int = 15
	n: int = 0

	def __init__(self,bot):
		self.bot = bot
		self.all_musics = self.what_playlist("chill")

	def play_music(self,music,voice):
		voice.stop() if voice.is_playing() else None
		sources = FFmpegPCMAudio(f'{os.getcwd()}/res/Musics/{self.all_playlist[self.switch_playlist]}/{music}')
		return voice.play(sources)

	def start_loop(self):
		""" start_loop() -> For join() function ans 🟢 Message reaction. """
		if not self.change_musique_loop.is_running():
			return self.change_musique_loop.start()

	def cancel_loop(self):
		""" cancel_loop() -> For leave() function ans 🔴 Message reaction. """
		if not self.change_musique_loop.is_being_cancelled():
			return self.change_musique_loop.stop()

	def change_music(self,op: str):
		self.all_voices[self.vocalChannel.id]["choice_musique"] += 1 if op == '+' else -1
		if (self.all_voices[self.vocalChannel.id]["choice_musique"] >= len(self.all_musics)-1) if op == '+' else (self.all_voices[self.vocalChannel.id]["choice_musique"] <= -1):
			self.all_voices[self.vocalChannel.id]["choice_musique"] = 0 if op == '+' else len(self.all_musics)-1

	def create_user_playlist(self,event,path):
		os.mkdir(f"{os.getcwd()}/res/Musics/favorites/{event.member.id}")
		with open(path,'x') as f:
			json.dump(self.template_favorites_musics,f)

	def what_playlist(self,playlist_name):
		self.all_musics = os.listdir(f"{os.getcwd()}/res/Musics/{playlist_name}")
		self.create_random_player()
		return self.all_musics

	async def edit_music_playlist_file(self,message,mode,path):
		with open(path) as f:
			data = json.load(f)
		if data["musics"].count(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]]) == (0 if mode == "set" else 1):
			with open(path,'w') as f:
				data["musics"].append(str(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]])) if mode == "set" else data["musics"].remove(str(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]]))
				return json.dump(data,f)
		return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous ne pouvez pas ajouté une musique dans vos favoris déjà existante"),delete_after=self.delete_after)

	async def leave(self,event,message,guild):
		""" leave() -> Function for 🔴 Message reaction. """
		# The bot leave the vocal channel
		if str(event.emoji) == self.bot.emoji_remove_bot:
			if self.all_voices[self.vocalChannel.id]["creator"] == event.member.id:
				await self.bot.change_activity(f"nothing | {self.bot.version}")
				self.cancel_loop()
				# leave vocal
				self.all_voices.pop(self.vocalChannel.id)
				return await guild.voice_client.disconnect()
			# If the member is not proprietary of the bot
			return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description="Seul la personne qui ma fait rejoindre dans sont vocal pourra me deconnecté"),delete_after=self.delete_after)

	async def join(self,event,message,guild):
		""" join() -> Function for 🟢 Message reaction. """
		# Remove reaction
		if str(event.emoji) not in [self.bot.emoji_random_music]:
			await message.remove_reaction(event.emoji,event.member)
		# "Error" management
		if len(self.bot.voice_clients) == 1:
			# Have not a channel
			if event.member.voice is None:
				return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous devez <#868456252685045760> pour pouvoir me prendre !"),delete_after=self.delete_after)
			# Have channel but, the bot as been taken by an other vocal channel
			return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Le bot que vous vouliez prendre est déjà utilisé ! Attendez qu'il se libere ou rejoingnez le vocal <#{self.voice.channel.id}>"),delete_after=self.delete_after)
		else:
			# Have not a channel
			if event.member.voice is None:
				return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous devez <#868456252685045760> pour pouvoir me prendre !"),delete_after=self.delete_after)
		# If is not joined in a vocal channel
		self.vocalChannel = utils.get(guild.voice_channels,id=event.member.voice.channel.id)
		self.all_voices[self.vocalChannel.id] = self.template
		# join vocal
		self.voice = await self.vocalChannel.connect()
		self.all_voices[self.vocalChannel.id]["joined"] = True
		self.all_voices[self.vocalChannel.id]["creator"] = event.member.id
		# set random value for first start of musique
		random_choice = random.randint(0,len(self.all_musics)-1)
		self.all_voices[self.vocalChannel.id]["choice_musique"] = random_choice
		# Play music and change activity
		self.play_music(self.all_musics[random_choice],self.voice)
		await self.bot.change_activity(f"musics 𝘊𝘩𝘪𝘭𝘭 & 𝘓𝘰-𝘍𝘪 | {self.bot.version}",'online')
		self.start_loop()

	async def next_music(self,event,message):
		""" next_music() -> Function for ⏭ Message reaction. """
		if str(event.emoji) == self.bot.emoji_next_music and (self.voice.is_playing()):
			if self.all_voices[self.vocalChannel.id]["creator"] == event.member.id:
				# If 🔀 Reaction is not selected
				if self.all_voices[self.vocalChannel.id]["random"] is False:
					self.change_music('+')
				# If the user have selected 🔀 Reaction
				else:
					# If the list have number
					if len(self.choice_random_musics) != 0:
						self.all_voices[self.vocalChannel.id]["choice_musique"] = random.choice(self.choice_random_musics)
						self.choice_random_musics.pop(self.all_voices[self.vocalChannel.id]["choice_musique"])
					# Recreate self.choice_random_musics list
					else:
						self.create_random_player()
				return self.play_music(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]],self.voice)
			# If the user isn't taken the bot
			return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous ne pouvez pas changé de musique, que <@{self.all_voices[self.vocalChannel.id]['creator']}>, donc celui qui m'a fait rejoindre dans un vocal pourra changé la musique\n\n_demandez lui poliment de changé la musique_"),delete_after=self.delete_after)

	async def back_music(self,event,message):
		""" back_music() -> Function for ⏮ Message reaction. """
		if str(event.emoji) == self.bot.emoji_previous_music and (self.voice.is_playing()):
			if self.all_voices[self.vocalChannel.id]["creator"] == event.member.id:
				self.change_music('-')
				return self.play_music(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]],self.voice)
			return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous ne pouvez pas changé de musique, que <@{self.all_voices[self.vocalChannel.id]['creator']}>, donc celui qui m'a fait rejoindre dans un vocal pourra changé la musique\n\n_demandez lui poliment de changé la musique_"),delete_after=self.delete_after)

	async def stop_music(self,event,message):
		""" stop_music() -> Function for ⏹ Message reaction. """
		if (str(event.emoji) == self.bot.emoji_stop_music) and (self.voice.is_playing()):
			if self.all_voices[self.vocalChannel.id]["creator"] == event.member.id:
				self.cancel_loop()
				return self.voice.stop()
			return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous ne pouvez pas changé de musique, que <@{self.all_voices[self.vocalChannel.id]['creator']}>, donc celui qui m'a fait rejoindre dans un vocal pourra arrêté la musique\n\n_demandez lui poliment d'arrêté la musique_"),delete_after=self.delete_after)

	async def resume_music(self,event,message):
		""" stop_music() -> Function for ▶ Message reaction. """
		# Restart the music where is been stopped
		if (str(event.emoji) == self.bot.emoji_resume_music) and (not self.voice.is_playing()):
			if self.all_voices[self.vocalChannel.id]["creator"] == event.member.id:
				self.start_loop()
				return self.play_music(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]],self.voice)
			return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous ne pouvez pas de relancé la musique, que <@{self.all_voices[self.vocalChannel.id]['creator']}>, donc celui qui m'a fait rejoindre dans un vocal pourra arrêté la musique\n\n_demandez lui poliment de relancé la musique_"),delete_after=self.delete_after)

	async def set_random_music_selection(self,event,message):
		""" set_random_music_selection() -> Function for 🔀 Message reaction enable. """
		# Enable random selection of music
		if str(event.emoji) == self.bot.emoji_random_music:
			if self.all_voices[self.vocalChannel.id]["creator"] == event.member.id:
				self.all_voices[self.vocalChannel.id]["random"] = True
			else:
				await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous ne pouvez pas mettre le mode aléatoire, que <@{self.all_voices[self.vocalChannel.id]['creator']}>, donc celui qui m'a fait rejoindre dans un vocal pourra arrêté la musique\n\n_demandez lui poliment de mettre le mode aléatoire la musique_"),delete_after=self.delete_after)

	async def remove_random_music_selection(self,event,message):
		""" remove_random_music_selection() -> Function for 🔀 Message reaction disable. """
		# Disable random selection of music
		if (str(event.emoji) == self.bot.emoji_random_music) and (event.member is not None):
			# If the reaction is added by the "creator"
			if self.all_voices[self.vocalChannel.id]["creator"] == event.member.id:
				self.all_voices[self.vocalChannel.id]["random"] = False
			else:
				await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous ne pouvez pas enlevé le mode aléatoire, que <@{self.all_voices[self.vocalChannel.id]['creator']}>, donc celui qui m'a fait rejoindre dans un vocal pourra arrêté la musique\n\n_demandez lui poliment de enlevé le mode aléatoire la musique_"),delete_after=self.delete_after)

	async def set_favorite_music(self,event,message):
		if str(event.emoji) == self.bot.emoji_add_favorite:
			path = os.path.join(f"{os.getcwd()}/res/Musics/favorites/{event.member.id}/","user_favorites_playlist.json")
			try:
				open(path).close()
			except FileNotFoundError:
				self.create_user_playlist(event,path)
				await self.edit_music_playlist_file(message,"set",path)
			else:
				await self.edit_music_playlist_file(message,"set",path)

	async def remove_favorite_music(self,event,message):
		if str(event.emoji) == self.bot.emoji_remove_favorite:
			path = os.path.join(f"{os.getcwd()}/res/Musics/favorites/{event.member.id}/","user_favorites_playlist.json")
			try:
				open(path).close()
			except FileNotFoundError:
				self.create_user_playlist(event,path)
			else:
				await self.edit_music_playlist_file(message,"remove",path)

	async def change_playlist(self,event,message):
		if str(event.emoji) == self.bot.emoji_change_playlist:
			if self.all_voices[self.vocalChannel.id]["creator"] != event.member.id:
				return await message.channel.send(embed=Embed(title="> ⚠ Attention !",description=f"Vous ne pouvez pas changé de playlist, que <@{self.all_voices[self.vocalChannel.id]['creator']}>, donc celui qui m'a fait rejoindre dans un vocal pourra changé la playlist\n\n_demandez lui poliment de enlevé la changé_"),delete_after=self.delete_after)
			self.switch_playlist += 1
			if self.switch_playlist > len(self.all_playlist):
				self.switch_playlist = 0
			self.all_musics = self.what_playlist(self.all_playlist[self.switch_playlist])
			if self.all_playlist[self.switch_playlist] == "favorites":
				path = os.path.join(f"{os.getcwd()}/res/Musics/favorites/{event.member.id}/","user_favorites_playlist.json")
				try:
					open(path).close()
				except FileNotFoundError:
					self.switch_playlist = 0
					self.all_musics = self.what_playlist(self.all_playlist[self.switch_playlist])
					self.create_random_player()
					return self.all_musics
				else:
					with open(path) as f:
						data = json.load(f)
						self.all_musics = data["musics"]
			self.create_random_player()
			return self.all_musics

	def create_random_player(self):
		# Write numbers for random selection
		for n in range(0, len(self.all_musics)-1):
			self.choice_random_musics.append(n)

	@commands.Cog.listener()
	async def on_ready(self):
		self.create_random_player()
		await self.change_activity_music.start()

	@commands.Cog.listener()
	async def on_raw_reaction_add(self,event):
		if event.member.bot is False:
			if event.message_id == self.bot.data[str(event.guild_id)]['message_radio_id']:
				guild = utils.get(self.bot.guilds,id=event.guild_id)
				textChannel = utils.get(guild.channels,id=event.channel_id)
				message = textChannel.get_partial_message(event.message_id)
				# The bot join the vocal channel where is the user
				if str(event.emoji) == self.bot.emoji_add_bot:
					return await self.join(event,message,guild)

				# If joined a vocal channel
				if self.all_voices[self.vocalChannel.id]["joined"]:
					await self.leave(event,message,guild)
					await self.next_music(event,message)
					await self.back_music(event,message)
					await self.stop_music(event,message)
					await self.resume_music(event,message)
					await self.change_playlist(event,message)
					await self.set_favorite_music(event,message)
					await self.remove_favorite_music(event,message)
					await self.set_random_music_selection(event,message)
				# Remove after an action on reaction below of radio message
				await message.remove_reaction(event.emoji,event.member) if str(event.emoji) not in [self.bot.emoji_random_music] else None

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self,event):
		if event.message_id == self.bot.data[str(event.guild_id)]['message_radio_id']:
			guild = utils.get(self.bot.guilds,id=event.guild_id)
			text_channel = utils.get(guild.channels,id=event.channel_id)
			message = text_channel.get_partial_message(event.message_id)

			if self.all_voices[self.vocalChannel.id]["joined"] and (event.message_id == self.bot.data[str(event.guild_id)]['message_radio_id']):
				# Radio message
				await self.remove_random_music_selection(event,message)

	@loop(seconds=3)
	async def change_musique_loop(self):
		await self.bot.wait_until_ready()
		# Changing automatically the music if the previous music is finished
		if self.voice.is_playing() is False:
			if self.all_voices[self.vocalChannel.id]["random"] is False:
				self.change_music('+')
			else:
				self.all_voices[self.vocalChannel.id]["choice_musique"] = random.randint(0,len(self.all_musics) - 1)
			self.play_music(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]],self.voice)
			# [music_title, file_extension]
			try:
				file,extensions = str(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]]).split('.')
			# If other point if present in the music title
			except ValueError:
				file,extensions,*other = str(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]]).split('.')
			await self.bot.change_activity(file,'online')

		self.all_voices[self.vocalChannel.id]["stopped"] = self.voice.is_paused()
		self.all_voices[self.vocalChannel.id]["resume"] = self.voice.is_playing()

	@loop(minutes=1)
	async def change_activity_music(self):
		await self.bot.wait_until_ready()
		try:
			self.all_voices[self.vocalChannel.id].items()
		except (AttributeError, KeyError):
			# If there are not music playing
			await self.bot.change_activity(f"nothing | {self.bot.version}")
		else:
			if self.all_voices[self.vocalChannel.id]["joined"]:
				# [music_title, file_extension]
				try:
					file,extensions = str(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]]).split('.')
				# If other point if present in the music title
				except ValueError:
					file,extensions,*other = str(self.all_musics[self.all_voices[self.vocalChannel.id]["choice_musique"]]).split('.')
				# Names activities
				names_act = [f"musics 𝘊𝘩𝘪𝘭𝘭 & 𝘓𝘰-𝘍𝘪 | {self.bot.version}",file]
				if self.n >= 2:
					self.n = 0
				await self.bot.change_activity(names_act[self.n],'online')
				self.n += 1

	@loop(minutes=1)
	async def check_inactive(self):
		await self.bot.wait_until_ready()
		for guild in self.bot.guilds:
			member = utils.get(guild.members,id=self.bot.bot_id)

			if member.voice is not None:
				if (self.count >= 3) or (self.voice.is_playing() is False):
					self.count = 0
				await guild.voice_client.disconnect() if (len(member.voice.channel.members) == 1) and (self.count == 2) else None
				self.count += 1
