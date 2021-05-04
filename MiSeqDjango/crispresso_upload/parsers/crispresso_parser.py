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

        print(file_path)

        return self.chunkify_files(file_path)

    def extract_well_information(self, dirname) -> dict:
        """Overrides ParserInterface.extract_well_information()"""

        print('dirname: ', dirname)

        well_name = os.path.basename(dirname)
        print('well_name: ', well_name)
        well_info = self.get_well_info(dirname)

        return { well_name : well_info}

        #elif os.path.isdir(filename):
        #    well_match = re.search(well_num_pattern, filename)
        #    if well_match:
        #        well_name = os.path.basename(os.path.dirname(filename))
        #        return {"name_" + well_name : well_name}

    def yield_well_info(self, dirname):
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
                        yield method(io_string)

    def get_well_info(self, dirname):

        well_info = dict()

        for method_result in self.yield_well_info(dirname):
            well_info.update(method_result)

        return well_info

    def check_file(self, filename):
        """Check which file has been opened, if no match discard."""

        alleles_freq_pattern = r'Alleles_frequency_table\.txt$'
        quant_pattern = r'Quantification_of_editing_frequency\.txt$'
        log_pattern = r'CRISPResso_RUNNING_LOG\.txt$'

        alleles_match = re.search(alleles_freq_pattern, filename)
        quant_match = re.search(quant_pattern, filename)
        log_match = re.search(log_pattern, filename)

        if alleles_match:
            return self.get_allele_data
        elif quant_match:
            return self.get_quant_data
        elif log_match:
            return self.check_log

    def reconstruct_file_structure(self, array) -> dict:
        """Takes in an array and reconstructs it into the expected format depending on the specific implementation"""

        data = {
            'summary': {
                '01': {
                    'percentages': 'quant_data',
                    'details': None
                }
            },
            'overview': {
                'summary': {
                    'AAA01_A': ['AAA01']
                }
            },
            'gene_exp': {
                'summary': {
                    'AAA01': ['AAA01_A']
                }
            },
            'efficiency': {
                'summary': {
                    'AAA01': {
                        'total': 9999,
                        'nhej': 7777
                    },
                    'AAA01_A': {
                        'total': 9999,
                        'nhej': 7777
                    },
                    'all': {
                        'total': 19998,
                        'nhej': 15554
                    }
                }
            },
            'designs': {
                'summary': {
                    'AAA01': ['AAA01_A']
                }
            },
            'designs_reverse': {
                'summary': {
                    'AAA01': ['1']
                }
            },
            'gene_crispr': {
                'summary': {
                    'AAA01': ['AAA01_A']
                }
            },
            'selection': 'All',
            'variables': {
                'y1': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                'y2': ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
            }
        }

        default_well = {
                'percentages': 'null',
                'details': 'null'
            }

        for well_dict in array:
            if well_dict is None:
                continue
            print('well_dict: ', well_dict)
            for well_num in range(384):
                well = "{:02d}".format(well_num +1)
                print('well: ', well)
                data['summary'][well] = dict()
                well_dict[well] = well_dict.get(well, default_well)
                for key in well_dict[well]:
                    print('key: ', key)
                    if key == 'percentages':
                        data['summary'][well]['percentages'] = well_dict[well][key]
                    elif key == 'details':
                        data['summary'][well]['details'] = well_dict[well][key]
                    elif key == 'log':
                        pass
        
        print('data: ', data)
        return data



    def get_quant_data(self, io_string) -> dict:
        """Returns the extracted data from the Quantification_of_editing_frequency.txt file"""

        lines = io_string.read().split('\n')

        processed_lines = list()

        for line in lines:
            processed_line = line.strip()
            processed_line = processed_line.replace(" ", ":")
            processed_lines.append(processed_line)

        try:
            data = {
                'unmod': processed_lines[1].split(':')[2],
                'nhej': processed_lines[2].split(':')[2],
                'hdr': processed_lines[3].split(':')[2],
                'mix': processed_lines[4].split(':')[3],
                'total': processed_lines[6].split(':')[2]
            }
            return {'percentages': data}
        except ValueError as exc:
            raise ValueError("Something went wrong when saving quant data to an object") from exc

    def get_allele_data(self, io_string) -> dict:
        """Gets the allele data from the alleles frequency table"""

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

    def check_log(self, io_string) -> dict:
        """Checks log for running errors"""
        io_string.read()
        return {'log': 'log_data_goes_here'}

    def get_lines_above_threshold(self, lines):
        """Returns the lines that have above the specified threshold for displaying the data"""
        iterlines = iter(lines)
        next(iterlines)

        for line in iterlines:
            if len(line.split('\t')) < 10:
                print('skipping line')
                continue
            if float(line.split('\t')[9]) > float(self.threshold_percent):
                yield line
