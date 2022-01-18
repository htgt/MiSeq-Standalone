
import os, re
from point_mutation import utils

class IndelParser:
	"""Extract indel data from indel_histogram.txt"""

	def load_directory(self, file_path, well, exp) -> dict:
		folder_regex = utils.generate_folder_regex(well)

		return self.open_histogram_file(file_path, exp, folder_regex)

	def get_histogram_data(self, io_string, exp, well_match) -> dict:
		if exp != 'All':
			if exp != well_match:
				return {}
		lines = io_string.read().split('\n')
		result = []
		min = len(lines)
		min_index = 0
		max_index = len(lines) - 2
		max = -(len(lines))
		i = 0

		
		for line in lines:
			if 'indel' in line or line == '':
				continue
			i += 1
			split_line = line.split('\t')
			cast_value = [0, 0]
			cast_value[0] = utils.safe_cast(split_line[0], int, 0)
			cast_value[1] = utils.safe_cast(split_line[1], int, 0)

			if cast_value[1] > 0:
				if cast_value[0] < min:
					min = cast_value[0]
					min_index = i
				if max < cast_value[0]:
					max = cast_value[0]
					max_index = i


			try:
				result.append({
					'indel': utils.safe_cast(cast_value[0], int, 0),
					'frequency': utils.safe_cast(cast_value[1], int, 0)
				})
			except IndexError:
				result.append({
					'indel': 0,
					'frequency': 0
				})

		result = result[min_index-1:max_index+1]

		exp_name = well_match if exp is not 'All' else exp

		return {
			exp_name: result
		}

	def open_histogram_file(self, well_folder_path, exp, regex):
		all_histo_data = dict()
		for histogram_data in utils.get_file_stream(well_folder_path, exp, regex, 'indel_histogram.txt', self.get_histogram_data):
			all_histo_data.update(histogram_data)

		return all_histo_data
