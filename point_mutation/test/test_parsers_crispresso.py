import os, io
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
                },
            },
            'summary_dict' : { 
                'KMT2A_1': {
                    'Experiment': 'KMT2A_1',
                    'Gene': 'KMT2A'
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
            'yield_well_info_data' : {
                    'details' : {    
                    'KMT2A_1': {
                        'class': 'Not Called',
                        'frameshift' : 0,
                        'status': 'Plated'
                    }
                }
            },
            'file_structure_data' : {
                'miseq' : 'testFiles',
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
            },
            'default_overview_data' : {
                'overview_data' : {
                    'summary' : dict()
                },
                'gene_exp' : {
                    'summary' : dict()
                },
                'designs_reverse' : {
                    'summary' : {
                        '1' : dict()
                    }
                },
                'designs' : {
                    'summary' : {
                        '1' : dict()
                    }
                },
                'gene_crispr' : {
                    'summary' : dict()
                },
                'genes' : set(),
                'experiments' : set()
            },
            'overview' : {
                'designs': {
                    'summary': {
                        '1': {
                            'KMT2A': ['KMT2A_1']
                        }
                    }
                },
                'designs_reverse': {
                    'summary': {
                        '1': {
                            'KMT2A': ['KMT2A_1']
                        }, 
                        'KMT2A': ['1']
                    }
                },
                'experiments': {'KMT2A_1'},
                'gene_crispr': {
                    'summary': {
                        'KMT2A': ['KMT2A_1']
                    }
                },
                'gene_exp': {
                    'summary': {
                        'KMT2A': ['KMT2A_1']
                    }
                },
                'genes': {'KMT2A'},
                'overview_data': {
                    'summary': {
                        'KMT2A_1': ['KMT2A']
                    }
                }
            },
            'overview_test_data' : [
                {
                    '1': {
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
                            }, 
                        'experiments': ['KMT2A_1'], 
                        'gene': ['KMT2A'], 
                        'overview_data': ['KMT2A_1', 'KMT2A']
                    }
                }
            ],
            'summary' : {
                'summary' : {
                    '01' : dict()
                }
            },
            'efficiency' : {
                'efficiency' : {
                    'summary': {
                        'KMT2A_1': {
                            'nhej': 360, 
                            'total': 8582
                            },
                        'all': {
                            'nhej': 360, 
                            'total': 8582
                        }
                    }
                }
            },
            'quant_data' : {
                'percentages': {
                    'KMT2A_1': {
                        'hdr': '0',
                        'mix': '0',
                        'nhej': '294',
                        'total': '7429',
                        'wt': '7135'
                    }
                }
            },
            'file_path': '../../testFiles',
            'file_name_info': ['1', 'KMT2A_1'],
            'exp': 'KMT2A_1',
            'allele_file_name' : 'Alleles_frequency_table.txt',
            'quant_file_name': 'Quantification_of_editing_frequency.txt',
            'key_percentages' : 'percentages',
            'quant_io_string_data' : io.StringIO('Quantification of editing frequency:\n\
	- Unmodified:7135 reads\n\
	- NHEJ:294 reads (3 reads with insertions, 28 reads with deletions, 272 reads with substitutions)\n\
	- HDR:0 reads (0 reads with insertions, 0 reads with deletions, 0 reads with substitutions)\n\
	- Mixed HDR-NHEJ:0 reads (0 reads with insertions, 0 reads with deletions, 0 reads with substitutions)\n\
\n\
Total Aligned:7429 reads '),
            'test_lines' : io.StringIO('Aligned_Sequence	Reference_Sequence	Phred_Quality	NHEJ	UNMODIFIED	HDR	n_deleted	n_inserted	n_mutated	#Reads	%Reads\n\
GAAAGTCCGGAAAGACAAGGAAGGAACACCTCCACTTACAAAAGAAGATAAGACAGTTGTCAGACAAAGCCCTCGAAGGATTAAGCCAGTTAGGATTATTCCTTCTTCAAAAAGGACAGATGCAACCATTGCTAAGCAACTCTTACAGAGGGCAAAAAAGGGGGCTCAAAAGAAAATTGAAAAAGAAGCAGCTCAGCTGCAGGGAAGAAAGGTGAAGACACAGGTCAAAAATATTCGACAGTTCATCATGCCT	GAAAGTCCGGAAAGACAAGGAAGGAACACCTCCACTTACAAAAGAAGATAAGACAGTTGTCAGACAAAGCCCTCGAAGGATTAAGCCAGTTAGGATTATTCCTTCTTCAAAAAGGACAGATGCAACCATTGCTAAGCAACTCTTACAGAGGGCAAAAAAGGGGGCTCAAAAGAAAATTGAAAAAGAAGCAGCTCAGCTGCAGGGAAGAAAGGTGAAGACACAGGTCAAAAATATTCGACAGTTCATCATGCCT	BCBBCEEECCCCFFFFFFFFFFGFGGGGGFGGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFFGFFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFFGGGGFFFFGGFFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFFGGGGGFFFFFFFFFFEEEEEEEBBBBB	False	True	False	0.0	0.0	0	6002	80.7914927984924\n\
GAAAGTCCGGAAAGACAAGGAAGGAACACCTCCACTTACAAAAGAAGATAAGACAGTTGTCAGACAAAGCCCTCGAAGGATTAAGCCAGTTAGGATTATTCCTTCTTCAAAAAGGACAGATGCAACCATTGCTAAGCAACTCTTACAGAGGGC-AAAAAGGGGGCTCAAAAGAAAATTGAAAAAGAAGCAGCTCAGCTGCAGGGAAGAAAGGTGAAGACACAGGTCAAAAATATTCGACAGTTCATCATGCCT	GAAAGTCCGGAAAGACAAGGAAGGAACACCTCCACTTACAAAAGAAGATAAGACAGTTGTCAGACAAAGCCCTCGAAGGATTAAGCCAGTTAGGATTATTCCTTCTTCAAAAAGGACAGATGCAACCATTGCTAAGCAACTCTTACAGAGGGCAAAAAAGGGGGCTCAAAAGAAAATTGAAAAAGAAGCAGCTCAGCTGCAGGGAAGAAAGGTGAAGACACAGGTCAAAAATATTCGACAGTTCATCATGCCT	BCCCCEEFCCCCFFFGGGGGFGGFGGGHGGGGGGGGGGGHGGGGFGGGGGGGGGGGGGGGGGGGGGGGGGHGGGFFGGFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHGGGHGGHGHGHGGGGHHGGGGHGGGHHHGGHGHHHHHHHGHGGFGGGGFFFFGGGFGHGGHHHGGHGGHHHGHGGGGGHGGGHGGGGGGGGGHHGGGHHHGHGGGGGGGGGGGGFFHGGGGGFFFFFFGGGEEFFEFEBBBBB	False	True	False	0.0	0.0	0	66	0.8884102840220757\n\
GAAAGTCCGGAAAGACAAGGAAGGAACACCTCCACTTACAAAAGAAGATAAGACAGTTGTCAGACAAAGCCCTCGAAGGATTAAGCCAGTTAGGATTATTCCTTCTTCAAAAAGGACAGATGCAACCATTGCTAAGCAACTCTTACAGAGGGCAAAAAAGGGGGCTCAAAAGAAAATTGAAAAAGAAGCAGCTCAGCTGCAGGGAAGAAAGGTGAAGACACAGGTAAAAAATATTCGACAGTTCATCATGCCT	GAAAGTCCGGAAAGACAAGGAAGGAACACCTCCACTTACAAAAGAAGATAAGACAGTTGTCAGACAAAGCCCTCGAAGGATTAAGCCAGTTAGGATTATTCCTTCTTCAAAAAGGACAGATGCAACCATTGCTAAGCAACTCTTACAGAGGGCAAAAAAGGGGGCTCAAAAGAAAATTGAAAAAGAAGCAGCTCAGCTGCAGGGAAGAAAGGTGAAGACACAGGTCAAAAATATTCGACAGTTCATCATGCCT	BCBBBEEEBCCCFFEFFFFFFFFFFGFGFFGGGGGGGGGGGFGGFGFFGGGGGGGGGGGFFGGGGGGFGGGGGGFFGFFGGGGGGFGFGGGGGGFGGGGGFGGGGGGGHGGHGGGHGHGGHHGGGGGGGGGGGGGGGHHGGGGHGHGGGGGGFFGGHGFFFFHGFFGGGGGGGGGGGGHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHFGGGGHFGFFFFFFGFEFFEEEEBBBBB	False	True	False	0.0	0.0	0	25	0.33651904697805896').read().split('\n'),
            'lines_above_threshold' : ['GAAAGTCCGGAAAGACAAGGAAGGAACACCTCCACTTACAAAAGAAGATAAGACAGTTGTCAGACAAAGCCCTCGAAGGATTAAGCCAGTTAGGATTATTCCTTCTTCAAAAAGGACAGATGCAACCATTGCTAAGCAACTCTTACAGAGGGCAAAAAAGGGGGCTCAAAAGAAAATTGAAAAAGAAGCAGCTCAGCTGCAGGGAAGAAAGGTGAAGACACAGGTCAAAAATATTCGACAGTTCATCATGCCT	GAAAGTCCGGAAAGACAAGGAAGGAACACCTCCACTTACAAAAGAAGATAAGACAGTTGTCAGACAAAGCCCTCGAAGGATTAAGCCAGTTAGGATTATTCCTTCTTCAAAAAGGACAGATGCAACCATTGCTAAGCAACTCTTACAGAGGGCAAAAAAGGGGGCTCAAAAGAAAATTGAAAAAGAAGCAGCTCAGCTGCAGGGAAGAAAGGTGAAGACACAGGTCAAAAATATTCGACAGTTCATCATGCCT	BCBBCEEECCCCFFFFFFFFFFGFGGGGGFGGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFFGFFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFFGGGGFFFFGGFFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFFGGGGGFFFFFFFFFFEEEEEEEBBBBB	False	True	False	0.0	0.0	0	6002	80.7914927984924']
        }

        self.parser = CrispressoParser()

        # extract summary data
        extract_summary_data_config = { 'return_value': self.data['summary_data']}
        self.patchers['extract_summary_data'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.extract_summary_data', **extract_summary_data_config)

        # chunkify files
        self.patchers['chunkify_files'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.chunkify_files')

        # get_file_name_info
        get_file_name_info_config = { 'return_value': self.data['file_name_info']}
        self.patchers['get_file_name_info'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.get_file_name_info', **get_file_name_info_config)

        # get_well_info
        get_well_info_config = { 'return_value': self.data['well_info']}
        self.patchers['get_well_info'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.get_well_info', **get_well_info_config)

        # walk
        walk_mock = MagicMock(side_effect=lambda *a, **kw: iter([('/dirpath', ['dirname',], ['filename',]), ('/dir/path', ['dirname2',], ['filename2',]),]))
        self.patchers['walk'] = patch('os.walk', new=walk_mock)
        #os.walk = MagicMock(return_value = [('/dirpath', ('dirname',), ('filename',))])
        #iter().__next__.return_value = [('/dirpath', ('dirname',), ('filename',))]

        # check_file
        check_file_config = { 'return_value': self.mocked_check_file_return_method }
        self.patchers['check_file'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.check_file', **check_file_config)

        # open
        open_mock = MagicMock(side_effect=lambda *a, **kw: 'io string value')
        self.patchers['open'] = patch('builtins.open', new=open_mock)

        # yield_well_info
        yield_well_info_config = { 'return_value' : [self.data['yield_well_info_data']]}
        self.patchers['yield_well_info'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.yield_well_info', **yield_well_info_config)

        # generate_overview
        self.patchers['generate_overview'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.generate_overview')

        # generate_summary
        self.patchers['generate_summary'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.generate_summary')

        # generate_efficiency
        self.patchers['generate_efficiency'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.generate_efficiency')

        # update_dict
        self.patchers['update_dict'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.update_dict')

        # append_list
        self.patchers['append_list'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.append_list')
        


    
    def test_load_directory_assert_successful(self):
        patchers = ['extract_summary_data', 'chunkify_files']

        self.start_patchers(patchers)

        self.parser.load_directory(self.data['file_path'])
        
        self.parser.extract_summary_data.assert_called_once_with(self.data['file_path'])
        self.parser.chunkify_files.assert_called_once_with(self.data['file_path'], self.data['summary_data'])

        self.stop_patchers(patchers)

    def test_extract_well_information_assert_successful_well(self):
        patchers = ['get_file_name_info', 'get_well_info']

        self.start_patchers(patchers)

        file_name = self.data['file_path'] + "/S1_expKMT2A_1"

        well_info = self.parser.extract_well_information(file_name, self.data['summary_dict'])

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

        well_info = self.parser.extract_well_information(file_name, self.data['summary_dict'])

        self.parser.get_file_name_info.assert_not_called()
        self.parser.get_well_info.assert_not_called()
        self.assertEqual(None, well_info)

        self.stop_patchers(patchers)

    def test_yield_well_info_assert_successful(self):
        patchers = ['open', 'check_file', 'walk']

        self.start_patchers(patchers)

        dir_name = self.data['file_path'] + '/S1_expKMT2A_1'

        values = list(self.parser.yield_well_info(dir_name, 'KMT2A_1'))

        self.parser.check_file.assert_called_with('filename')
        self.assertEqual(values[0][0], 'io string value')
        self.assertEqual(values[0][1], 'KMT2A_1')

        self.stop_patchers(patchers)

    def test_get_well_info_assert_successful(self):
        patchers = ['yield_well_info']
        self.start_patchers(patchers)

        dir_name = self.data['file_path'] + '/S1_expKMT2A_1'

        well_info = self.parser.get_well_info(dir_name, self.data['exp'])

        self.assertEqual(well_info, self.data['yield_well_info_data'])
        self.parser.yield_well_info.assert_called_with(dir_name, self.data['exp'])

        self.stop_patchers(patchers)

    def test_check_file_assert_allele_successful(self):
        patchers = ['']
        self.start_patchers(patchers)

        method = self.parser.check_file(self.data['allele_file_name'])

        self.assertEqual(self.parser.get_allele_data, method)

        self.stop_patchers(patchers)

    def test_check_file_assert_quant_successful(self):
        patchers = ['']
        self.start_patchers(patchers)

        method = self.parser.check_file(self.data['quant_file_name'])

        self.assertEqual(self.parser.get_quant_data, method)

        self.stop_patchers(patchers)

    def test_reconstruct_file_structure_assert_large_plate_successful(self):
        patchers = ['generate_overview', 'generate_summary']
        self.start_patchers(patchers)

        array = range(384)
        self.data['file_structure_data']['large_plate'] = True

        file_structure_data = self.parser.reconstruct_file_structure(array, self.data['file_path'] + '/S1_expKMT2A_1')

        self.assertEqual(file_structure_data['large_plate'], True)
        self.parser.generate_overview.assert_called_once_with(array, self.data['file_structure_data'])
        self.parser.generate_summary.assert_called_once_with(array, self.data['file_structure_data'])
        self.assertEqual(file_structure_data, self.data['file_structure_data'])

        self.stop_patchers(patchers)

    def test_reconstruct_file_structure_assert_standard_plate_successful(self):
        patchers = ['generate_overview', 'generate_summary']
        self.start_patchers(patchers)

        array = range(96)
        self.data['file_structure_data']['large_plate'] = False

        file_structure_data = self.parser.reconstruct_file_structure(array, self.data['file_path'] + '/S1_expKMT2A_1')

        self.assertEqual(file_structure_data['large_plate'], False)
        self.parser.generate_overview.assert_called_once_with(array, self.data['file_structure_data'])
        self.parser.generate_summary.assert_called_once_with(array, self.data['file_structure_data'])
        self.assertEqual(file_structure_data, self.data['file_structure_data'])

        self.stop_patchers(patchers)

    def test_generate_overview_assert_successful(self):
        patchers = ['']
        self.start_patchers(patchers)

        array = self.data['overview_test_data']
        test_data = self.data['default_overview_data']

        self.parser.generate_overview(array, test_data)

        self.assertEqual(test_data, self.data['overview'])

        self.stop_patchers(patchers)

    def test_generate_summary_assert_successful(self):
        patchers = ['update_dict', 'append_list', 'generate_efficiency']
        self.start_patchers(patchers)

        array = self.data['overview_test_data']
        test_data = {
            'summary' : {
            }
        }

        self.parser.generate_summary(array, test_data)

        self.assertEqual(test_data, self.data['summary'])

        self.stop_patchers(patchers)

    def test_generate_efficiency_assert_successful(self):
        patchers = ['']
        self.start_patchers(patchers)

        test_data = {
            'efficiency' : {
                'summary' : dict()
            }
        }

        self.parser.generate_efficiency(test_data, self.data['overview_test_data'][0], '1', self.data['key_percentages'])

        self.assertEqual(test_data, self.data['efficiency'])

        self.stop_patchers(patchers)

    def test_get_quant_data_assert_successful(self):
        patchers = ['']
        self.start_patchers(patchers)

        quant_data = self.parser.get_quant_data(self.data['quant_io_string_data'], self.data['exp'])

        self.assertEqual(quant_data, self.data['quant_data'])

        self.stop_patchers(patchers)

    def test_get_lines_above_threshold_assert_successful(self):
        patchers = ['']
        self.start_patchers(patchers)

        self.parser.threshold_percent = 70

        lines_above_threshold = list(self.parser.get_lines_above_threshold(self.data['test_lines']))

        self.assertEqual(lines_above_threshold, self.data['lines_above_threshold'])

        self.stop_patchers(patchers)

    ### setup methods

    def mocked_check_file_return_method(self, io_string, exp):
        return [io_string, exp]

    def start_patchers(self, patchers_to_start):
        if patchers_to_start:
            for patcher in patchers_to_start:
                if patcher:
                    self.patchers[patcher].start()

    def stop_patchers(self, patchers_to_stop):
        if patchers_to_stop:
            for patcher in patchers_to_stop:
                if patcher: 
                    self.patchers[patcher].stop()