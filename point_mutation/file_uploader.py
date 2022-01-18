import os
from django.core.files import File

class FileUploader:
	def handle_files(self, relative_path, file):
		
		self.save_files(relative_path, file)


	def reconstruct_file_structure(self, directories, files):
		directory_structure = {}

		for file in files:

			directory_structure[list(directories.keys())[list(directories.values()).index(file.name)]] = file

		return directory_structure

	def save_files(self, relative_path, file):
		save_path = "/var/data/uploadedFiles/" + relative_path
		#complete_name = os.path.join(save_path, str(file))
		dirname = os.path.dirname(save_path)
		os.makedirs(dirname, exist_ok=True)
		raw = file.read()#.encode('ISO-8859-1')
		with open(save_path, 'wb+') as f:
			f.write(raw)

	def expand_directories(self, flat_directories):
		#print(flat_directories)
		directories = {}
		flat_directories = flat_directories.replace('"', '')
		flat_directories = flat_directories.replace('{', '')
		flat_directories = flat_directories.replace('}', '')
		kvps = flat_directories.split(',')
		for kvp in kvps:
			key, value = kvp.split(':')
			directories[value] = key #This way as the values are unique but keys may not be.

		return directories
