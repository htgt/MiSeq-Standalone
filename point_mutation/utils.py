import os, re

def safe_cast(val, to_type, default=None):
	try:
		return to_type(val)
	except (ValueError, TypeError):
		return default

complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'} 

def reverse_complement(seq):    
    bases = list(seq) 
    bases = reversed([complement.get(base,base) for base in bases])
    bases = ''.join(bases)
    return bases

def get_crispr_position(crispr, rev_crispr, amplicon):
	position = 0
	upper_amplicon = amplicon.upper()
	if crispr in upper_amplicon:
		position = upper_amplicon.index(crispr)
	else:
		if rev_crispr in upper_amplicon:
			position = upper_amplicon.index(rev_crispr)

	return position

def get_file_stream(well_folder_path, exp, regex, file_name, method):
		subdirs = [x[0] for x in os.walk(well_folder_path)]
		for subdir in subdirs:
			well_match = re.search(regex, subdir)
			if not well_match:
				continue
			files = None
			try:
				files = os.walk(subdir).__next__()[2]
			except StopIteration:
				pass
			if (len(files) > 0):
				for file in files:
					if file == file_name:
						filename = os.path.join(subdir, file)
						io_string = open(filename, "r", encoding="utf-8")
						yield method(io_string, exp, well_match.group(1))

def generate_folder_regex(well):
		regex = "S" + well.lstrip("0") + "_exp(.*)/.*$"

		return regex