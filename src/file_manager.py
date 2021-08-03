import os
import json
import datetime
import shutil
import configparser

from typing import Optional


def try_load(func):
	def load_file(*args,**kwargs):
		obj,file,directory = args
		path = os.path.join(directory,file)
		try:
			open(path).close()
		except (FileNotFoundError,OSError) as e:
			return print(obj.msg_error_read(file),f"\nDetails: {e}"),quit()
		else:
			return func(*args,**kwargs)

	return load_file


class FileManager(object):

	def __init__(self):
		self.msg_error_read = lambda file: f"Les données n'ont pas pu êtres lu car le fichier {file} n'a pas étais trouvé !"
		self.msg_error_write = lambda file: f"Les données n'ont pas pu êtres ecrit car le fichier {file} n'a pas étais trouvé !"

	@try_load
	def load(self,file: str,directory: Optional[str] = os.getcwd()):
		""" load( ) -> Load a file.
				:param file: Specify the name of your file with his extension.
				:param directory: Specify a directory to going access at your file. """
		name,extension = file.split('.')
		path = os.path.join(directory,file)

		if extension == 'json':
			with open(path) as f:
				data = json.load(f)
			return data
		if extension == 'ini':
			data = configparser.ConfigParser()
			data.read(f"{directory}{file}", encoding="UTF-8")
			return data

	@try_load
	def write(self,data,file: str,directory: Optional[str] = os.getcwd()):
		""" write( ) -> Write a file.
				:param data: Specify a variable which contain your data at write.
				:param file: Specify the name of your file with his extension.
				:param directory: Specify a directory to going acces at your file. """
		name,extension = file.split('.')
		path = os.path.join(directory,file)

		if extension == 'json':
			with open(path,'w') as f:
				json.dump(data,f)
		if extension == 'ini':
			data.write(path)

	def copy(self,origin_dir: str,origin_file: str,backup_dir: str,backup_file: str = None):
		""" * Permet de copier un fichier correctement et simplement
				:param origin_dir: Le chemin d'accès original de votre fichier
				:param origin_file: Le nom de votre fichier d'origine
				:param backup_dir: Le chemin d'accès où le fichier copie va êtres
				:param backup_file: Le nom de votre fichier copie """
		# Si il y a pas de nom specifié
		if backup_file is None:
			date,hour = str(datetime.datetime.today()).split(' ')
			h,m,s = hour.split(':')
			new_hour = f'{h}-{m}-{round(float(s))}'
			backup_file = f'{origin_file}[{date}_{new_hour}]'

		origin_file_path = os.path.join(origin_dir,origin_file)
		backup_file_path = os.path.join(backup_dir,backup_file)
		# Crée le fichier
		with open(backup_file_path,'x'):
			shutil.copy(origin_file_path,backup_file_path)
