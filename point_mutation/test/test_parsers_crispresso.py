from django.test import SimpleTestCase

from unittest.mock import MagicMock, patch

from point_mutation.parsers.crispresso_parser import CrispressoParser


class CrispressoParserTestCase(SimpleTestCase):
    data = None
    parser = None
    patchers = {}

    def setUp(self):
        self.data = {
            'summary_data' : { 
                'KMT2A_1': {
                    'Experiment': 'KMT2A_1',
                    'Gene': 'KMT2A',
                    'Crispr': 'CTCGAAGGATTAAGCCAGTT',
                    'Strand': '+',
                    'Amplicon': 'GAAAGTCCGGAAAGACAAGGAAGgaacacctccacttacaaaagaagataagacagttgtcagacaaagccctcgaaggattaagccagttaggattattccttcttcaaaaaggacagatgcaaccattgctaagcaactcttacagagggcaaaaaagggggctcaaaagaaaattgaaaaagaagcagctcagctgcagggaagaaaggtgaagacacaggtcaaaaATATTCGACAGTTCATCATGCCT',
                    'min_index': '1',
                    'NHEJ': '76791',
                    'Total': '573759',
                    'max_index': '96'
                }
            },
            'well_info': {
                'percentages': {
                    'KMT2A_1' : {
                        'wt': '8222', 
                        'nhej': '360', 
                        'hdr': '0', 
                        'mix': '0', 
                        'total': '8582'
                    }
                }, 
                'details': {
                    'KMT2A_1': {
                        'class': 'Not Called', 
                        'frameshift': 0, 
                        'status': 'Plated'
                    }
                }
            },
            'file_path': '../../testFiles',
            'file_name_info': ['1', 'KMT2A_1']
        }

        self.parser = CrispressoParser()

        # extract summary data
        extract_summary_data_config = { 'method.return_value': self.data['summary_data']}
        self.patchers['extract_summary_data'] = patch('CrispressoParser.extract_summary_data', **extract_summary_data_config)

        # chunkify files
        self.patchers['chunkify_files'] = patch('CrispressoParser.chunkify_files')

        # get_file_name_info
        get_file_name_info_config = { 'method.return_value': self.data['file_name_info']}
        self.patchers['get_file_name_info'] = patch('CrispressoParser.get_file_name_info', **get_file_name_info_config)

        # get_well_info
        get_well_info_config = { 'method.return_value': self.data['well_info']}
        self.patchers['get_well_info'] = patch('CrispressoParser.get_well_info', **get_well_info_config)

        # walk
        walk_config = { 'method.return_value': [['dirpath'], ['dirname'], ['filename']]}
        self.patchers['walk'] = patch('os.walk', **walk_config)

        # check_file
        check_file_config = { 'method.return_value': self.mocked_check_file_return_method }
        self.patchers['check_file'] = patch('CrispressoParser.check_file', **check_file_config)

        # open
        open_config = { 'method.return_value': 'io string value' }
        self.patchers['open_config'] = patch('__main__.open', **open_config)


    
    def test_load_directory_assert_successful(self):
        patchers = ['extract_summary_data', 'chunkify_files']

        self.start_patchers(patchers)

        self.parser.load_directory(self.data['file_path'])
        
        self.parser.extract_summary_data.assert_called_once_with(self.data['file_path'])
        self.parser.chunkify_files.assert_called_once_with(self.data['file_path', self.data['sumamry_data']])

        self.stop_patchers(patchers)

    def test_extract_well_information_assert_successful_well(self):
        patchers = ['get_file_name_info', 'get_well_info']

        self.start_patchers(patchers)

        file_name = self.data['file_path'] + "/S1_expKMT2A_1"

        well_info = self.parser.extract_well_information(file_name, self.data['summary_data'])

        self.parser.get_file_name_info.assert_called_once_with('S1_expKMT2A_1')
        self.parser.get_well_info.assert_called_once_with(file_name, 'KMT2A_1')
        self.assertEqual(well_info['1']['experiments'], ['KMT2A_1'])
        self.assertEqual(well_info['1']['gene'], ['KMT2A'])
        self.assertEqual(well_info['1']['overview_data'], ['KMT2A_1', 'KMT2A'])

        self.stop_patchers(patchers)

    def test_extract_well_information_assert_successful_summary(self):
        patchers = ['get_file_name_info', 'get_well_info']

        self.start_patchers(patchers)

        file_name = self.data['file_path'] + "/summary.csv"

        well_info = self.parser.extract_well_information(file_name, self.data['summary_data'])

        self.parser.get_file_name_info.assert_not_called()
        self.parser.get_well_info.assert_not_called()
        self.assertEqual(None, well_info)

        self.stop_patchers(patchers)

    def test_yield_well_info_assert_successful(self):
        patchers = ['open', 'walk', 'check_file']

        self.start_patchers(patchers)

        dir_name = self.data['file_name'] + '/S1_expKMT2A_1'

        values = self.parser.yield_well_info(dir_name, 'KMT2A_1')

        self.parser.check_file.assert_called_with('filename')
        self.assertEqual(values[0], 'io string value')
        self.assertEqual(values[1], 'KMT2A_1')

        self.stop_patchers(patchers)

    ### Mocked methods

    def mocked_extract_summary_data(self, *args):
        return self.data['summary_data']

    def mocked_chunkify_files(*args):
        input_values = []
        for arg in args:
            input_values.append(arg)

        return input_values

    def mocked_get_file_name_info(self, *args):
        return self.data['file_name_info']
    
    def mocked_get_well_info(self, *args):
        return self.data['well_info']

    def mocked_check_file_return_method(self, io_string, exp):
        return [io_string, exp]

    def start_patchers(self, patchers_to_start):
        for patcher in patchers_to_start:
            self.patchers[patcher].start()

    def stop_patchers(self, patchers_to_stop):
        for patcher in patchers_to_stop:
            self.patchers[patcher].stop()