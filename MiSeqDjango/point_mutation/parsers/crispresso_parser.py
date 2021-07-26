"""Contains methods for the CRISPResso implementation of the parser"""

import os
import re

from .parser_interface import ParserInterface

class CrispressoParser(ParserInterface):
    """Extract data from CRISPResso tar file."""

    global_threshold = 0
    threshold_percent = 0

    def load_directory(self, file_path) -> dict:
        """Overrides ParserInterface.load_tar_file()"""
        if not file_path:
            file_path = self.DEFAULT_DIR

        summary_dict = self.extract_summary_data(file_path)

        return self.chunkify_files(file_path, summary_dict)

    def extract_well_information(self, dirname, summary_dict) -> dict:
        """Overrides ParserInterface.extract_well_information()"""


        file_name = os.path.basename(dirname)

        if file_name == "summary.csv":
            return None
        
        file_name_info = self.get_file_name_info(file_name)
        exp = file_name_info[1]
        gene = summary_dict[exp]['Gene'].split('_')[0]

        well_info = self.get_well_info(dirname, exp)

        if len(well_info) != 0:
            well_info.update({ 
                            'experiments' : [ exp ] ,
                            'gene' : [ gene ],
                            'overview_data' : [ exp , gene ]
                        })
        
        return { file_name_info[0] : well_info}

        #elif os.path.isdir(filename):
        #    well_match = re.search(well_num_pattern, filename)
        #    if well_match:
        #        well_name = os.path.basename(os.path.dirname(filename))
        #        return {"name_" + well_name : well_name}

    def yield_well_info(self, dirname, exp):
        """Returns a generator object that contains the well information."""
        
        subdirs = [x[0] for x in os.walk(dirname)]                                                                            
        for subdir in subdirs:
            files = os.walk(subdir).__next__()[2]
            if (len(files) > 0):
                for file in files:
                    method = self.check_file(file)

                    if method is not None:
                        filename = os.path.join(subdir, file)
                        io_string = open(filename, "r", encoding="utf-8")
                        yield method(io_string, exp)

    def get_well_info(self, dirname, exp):

        well_info = dict()

        for method_result in self.yield_well_info(dirname, exp):
            well_info.update(method_result)

        return well_info

    def check_file(self, filename):
        """Check which file has been opened, if no match discard."""

        alleles_freq_pattern = r'Alleles_frequency_table\.txt$'
        quant_pattern = r'Quantification_of_editing_frequency\.txt$'

        alleles_match = re.search(alleles_freq_pattern, filename)
        quant_match = re.search(quant_pattern, filename)

        if alleles_match:
            return self.get_allele_data
        elif quant_match:
            return self.get_quant_data

    def reconstruct_file_structure(self, array, file_path) -> dict:
        """Takes in an array and reconstructs it into the expected format depending on the specific implementation"""
        large_plate = len(array) > 96

        folder_name = os.path.basename(os.path.dirname(file_path))

        data = {
            'large_plate': large_plate,
            'miseq' : folder_name,
            'summary': {
            },
            'overview_data': {
                'summary': {
                }
            },
            'gene_exp': {
                'summary': {
                }
            },
            'efficiency': {
                'summary': {
                }
            },
            'designs': {
                'summary': {
                    '1' : {}
                }
            },
            'designs_reverse': {
                'summary': {
                    '1' : {}
                }
            },
            'gene_crispr': {
                'summary': {
                    'AAA01': ['AAA01_A']
                }
            },
            'genes' : set(),
            'experiments' : set(),
            'selection': 'All',
            'variables': {
                'y1': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                'y2': ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
            }
        }




        self.generate_overview(array, data)
        self.generate_summary(array, data)


        return data

    def generate_overview(self, array, data):

        for well_dict in array:
            if well_dict is None:
                continue
            for well_num in well_dict:
                if 'overview_data' in well_dict[well_num]:
                    exp, gene = well_dict[well_num]['overview_data']

                    data['overview_data']['summary'][exp] = data['overview_data']['summary'].get(exp, [])
                    data['gene_exp']['summary'][gene] = data['overview_data']['summary'].get(gene, [])

                    data['overview_data']['summary'][exp] = [gene]
                    data['gene_exp']['summary'][gene].append(exp)

                    data['genes'].add(gene)
                    data['experiments'].add(exp)

                    data['designs_reverse']['summary'][gene] = ['1']
                    data['designs_reverse']['summary']['1'][gene] = data['designs_reverse']['summary']['1'].get(gene, [])
                    designs_reverse_set = set(data['designs_reverse']['summary']['1'][gene])
                    designs_reverse_set.add(exp)
                    data['designs_reverse']['summary']['1'][gene] = list(designs_reverse_set)

                    data['designs']['summary']['1'][gene] = data['designs']['summary']['1'].get(gene, [])
                    designs_set = set(data['designs']['summary']['1'][gene])
                    designs_set.add(exp)
                    data['designs']['summary']['1'][gene] = list(designs_set)

                    data['gene_crispr']['summary'][gene] = data['gene_crispr']['summary'].get(gene, [])
                    gene_crispr_set = set(data['gene_crispr']['summary'][gene])
                    gene_crispr_set.add(exp)
                    data['gene_crispr']['summary'][gene] = list(gene_crispr_set)

                    




    def generate_efficiency(self, data, well_dict, well_num, key):
        if key == 'percentages':
            for exp in well_dict[well_num][key]:
                data['efficiency']['summary'][exp] = data['efficiency']['summary'].get(exp, {})
                data['efficiency']['summary'][exp] = {
                                'nhej' : data['efficiency']['summary'][exp].get('nhej', 0) + int(well_dict[well_num][key][exp].get('nhej', 0)),
                                'total': data['efficiency']['summary'][exp].get('total', 0) + int(well_dict[well_num][key][exp].get('total', 0))
                            }
                data['efficiency']['summary']['all'] = data['efficiency']['summary'].get('all', {})
                data['efficiency']['summary']['all'] = {
                                'nhej' : data['efficiency']['summary']['all'].get('nhej', 0) + int(well_dict[well_num][key][exp].get('nhej', 0)),
                                'total': data['efficiency']['summary']['all'].get('total', 0) + int(well_dict[well_num][key][exp].get('total', 0))
                            }


    def generate_summary(self, array, data):
        define_well_data = {
            'details' : self.update_dict,
            'percentages' : self.update_dict,
            'experiments' : self.append_list,
            'gene' : self.append_list,
            'overview_data' : self.append_list
        }

        for well_dict in array:
            if well_dict is None:
                continue
            for well_num in well_dict:
                well_num_copy = well_num
                well = "{:02d}".format(int(well_num_copy))
                data['summary'][well] = data['summary'].get(well, dict())
                for key in well_dict[well_num]:
                    define_well_data[key](data, well_dict, well_num, well, key)
                    self.generate_efficiency(data, well_dict, well_num, key)

    def append_list(self, data, well_dict, well_num, well, key):
        default_data = []
        data['summary'][well][key] = data['summary'][well].get(key, default_data)
        data['summary'][well][key].extend(well_dict[well_num][key])

    def update_dict(self, data, well_dict, well_num, well, key):
        default_data = {}
        data['summary'][well][key] = data['summary'][well].get(key, default_data)
        data['summary'][well][key].update(well_dict[well_num][key])



    def get_quant_data(self, io_string, exp) -> dict:
        """Returns the extracted data from the Quantification_of_editing_frequency.txt file"""

        lines = io_string.read().split('\n')

        processed_lines = list()

        for line in lines:
            processed_line = line.strip()
            processed_line = processed_line.replace(" ", ":")
            processed_lines.append(processed_line)

        try:
            data = {
                exp: {
                    'wt': processed_lines[1].split(':')[2],
                    'nhej': processed_lines[2].split(':')[2],
                    'hdr': processed_lines[3].split(':')[2],
                    'mix': processed_lines[4].split(':')[3],
                    'total': processed_lines[6].split(':')[2]
                }
            }
            return {'percentages': data}
        except ValueError as exc:
            raise ValueError("Something went wrong when saving quant data to an object") from exc

    def get_allele_data(self, io_string, exp) -> dict:
        """Gets the allele data from the alleles frequency table"""

        return {
                    'details' : {
                        exp: {
                            'class': 'Not Called',
                            'frameshift' : 0,
                            'status': 'Plated'
                        }
                    }
                }


        lines = io_string.read().split('\n')
        threshold = self.global_threshold or 0

        processed_lines = list()

        if self.threshold_percent:
            for line in self.get_lines_above_threshold(lines):
                processed_lines.append(line)
        elif threshold != 0:
            line_limit = min(threshold, len(lines))
            processed_lines = lines[0:line_limit]

        return {'details': processed_lines}

    def get_lines_above_threshold(self, lines):
        """Returns the lines that have above the specified threshold for displaying the data"""
        iterlines = iter(lines)
        next(iterlines)

        for line in iterlines:
            if len(line.split('\t')) < 10:
                continue
            if float(line.split('\t')[9]) > float(self.threshold_percent):
                yield line


    def get_file_name_info(self, file_name):
        match = re.search("^S([\d]+)_exp(.+$)", file_name)


        return [match.group(1), match.group(2)]
    