from re import L
from point_mutation import utils

class FrequencyParser:
	def get_allele_freq_data(self, file_path, well_num, exp, limit):
		return self.load_directory(file_path, well_num, exp, limit)

	def load_directory(self, file_path, well, exp, limit) -> dict:
		regex = utils.generate_folder_regex(well)

		if limit == 'All':
			limit = int(float('inf')) - 1
		
		lines = []
		for allele_data in utils.get_file_stream(file_path, exp, regex, 'Alleles_frequency_table.txt', self.get_allele_data):
			if allele_data is None: 
				continue
			for x in range(int(limit)+1):
				lines.append(allele_data[x])

		return str.join('\n', lines)

	def get_allele_data(self, io_string, exp, well_match):
		if exp == well_match:
			return io_string.read().split('\n')

		
