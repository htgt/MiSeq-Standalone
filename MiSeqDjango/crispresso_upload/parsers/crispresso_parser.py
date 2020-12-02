"""Contains methods for the CRISPResso implementation of the parser"""

import tarfile
import re

from .parser_interface import ParserInterface

class CrispressoParser(ParserInterface):
    """Extract data from CRISPResso tar file."""

    global_threshold = 0
    threshold_percent = 0

    def load_tar_file(self, file: tarfile, uploaded_file_path) -> dict:
        """Overrides ParserInterface.load_tar_file()"""
        with file.open(uploaded_file_path, 'r|*') as tar:
            return self.chunkify_tar_file(tar)

    def extract_well_information(self, file, tar_info) -> dict:
        """Overrides ParserInterface.extract_well_information()"""

        well_num_pattern = r'/(\d{2})/$'

        if tar_info.isfile():
            method = self.check_file(tar_info)
            
            if method is not None:
                io_string = file.extractfile(tar_info)
                return method(io_string)

        elif tar_info.isdir():
            well_match = re.search(well_num_pattern, tar_info.name)
            if well_match:
                return {"name_" + well_match.group(0) : well_match.group(0)}

    def check_file(self, tar_info):
        """Check which file has been opened, if no match discard."""

        alleles_freq_pattern = r'Alleles_frequency_table\.txt$'
        quant_pattern = r'Quantification_of_editing_frequency\.txt$'
        log_pattern = r'CRISPResso_RUNNING_LOG\.txt$'

        alleles_match = re.search(alleles_freq_pattern, tar_info.name)
        quant_match = re.search(quant_pattern, tar_info.name)
        log_match = re.search(log_pattern, tar_info.name)

        if alleles_match:
            return self.get_allele_data
        elif quant_match:
            return self.get_quant_data
        elif log_match:
            return self.check_log

    def reconstruct_file_structure(self, array) -> dict:
        """Takes in an array and reconstructs it into the expected format depending on the specific implementation"""
        well_key_pattern = r'name_(\d{2})$'

        data = {
            "summary": {
                "01": {
                    "percentages": "quant_data"
                }
            }
        }
        for item in array:
            key_match = re.search(well_key_pattern, item.key)
            current_well = "00"
            if key_match:
                current_well = key_match.group(0)
            elif item.key == "quant_data":
                data["summary"][current_well]["percentages"] = item.value
            elif item.key == "lines":
                pass
            elif item.key == "log":
                pass
                



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
                "unmod": processed_lines[1].split(':')[2],
                "nhej": processed_lines[2].split(':')[2],
                "hdr": processed_lines[3].split(':')[2],
                "mix": processed_lines[4].split(':')[3],
                "total": processed_lines[6].split(':')[2]
            }
            return {"quant_data": data}
        except ValueError as exc:
            raise ValueError("Something went wrong when saving quant data to an object") from exc

    def get_allele_data(self, io_string) -> dict:
        """Gets the allele data from the alleles frequency table"""

        lines = io_string.read().split('\n')
        threshold = self.global_threshold or 0

        processed_lines = list()

        if self.threshold_percent:
            processed_lines = self.get_lines_above_threshold(lines)
        elif threshold != 0:
            line_limit = min(threshold, len(lines))
            processed_lines = lines[0:line_limit]

        return {"lines": processed_lines}

    def check_log(self, io_string) -> dict:
        """Checks log for running errors"""
        io_string.read()
        return {"log": "log_data_goes_here"}

    def get_lines_above_threshold(self, lines):
        """Returns the lines that have above the specified threshold for displaying the data"""

        for line in lines:
            if float(line.split(',')[9]) > float(self.threshold_percent):
                yield line
