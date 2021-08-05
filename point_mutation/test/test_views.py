import os
from django import test
from django.http.response import HttpResponse
from django.test import SimpleTestCase, Client
from django.http import request
from django.test.client import RequestFactory

from unittest.mock import MagicMock, patch

import point_mutation.views


class ViewsTestCase(SimpleTestCase):
    data = None
    client = Client()
    request_factory = None
    session_factory = None
    patchers = {}

    ### setup methods
    def setUp(self):
        self.request_factory = RequestFactory()
        post_data = {
            'folderPath' : 'folder/path/',
            'item' : 'item'
            }

        self.data = {
            'successful_http_response_code' : 200,
            'get_request' : self.request_factory.get('/get/request'),
            'post_request' : self.request_factory.post('/', post_data),
            'get_dirs_data' : 'This is a dir',
            'folder_path' : 'This is a folder path',
            'point_mutation_summary_data' : 'summary_data',
            'discover_folders_data' : {
                'folders' : 'folders_discovered'
            }
        }


        # get_dirs
        get_dirs_config = { 'return_value': self.data['get_dirs_data']}
        self.patchers['get_dirs'] = patch('point_mutation.discover.DiscoverFolders.get_dirs', **get_dirs_config)

        # discover_folders
        discover_folders_config = { 'return_value': self.data['discover_folders_data']}
        self.patchers['discover_folders'] = patch('point_mutation.views.discover_folders', **discover_folders_config)

        # point_mutation_summary
        point_mutation_summary_config = { 'return_value' : self.data['point_mutation_summary_data']}
        self.patchers['point_mutation_summary'] = patch('point_mutation.views.point_mutation_summary', **point_mutation_summary_config)

        # point_mutation_view
        test_request = self.client.post('/')
        test_request.status_code = 200
        point_mutation_view_config = { 'return_value' : test_request }
        self.patchers['point_mutation_view'] = patch('point_mutation.views.point_mutation_view', **point_mutation_view_config)

        #load_directory
        load_directory_config = { 'return_value' : {'summary' : {'01' : {'percentages' : 'quant_data_test' }}}}
        self.patchers['load_directory'] = patch('point_mutation.parsers.crispresso_parser.CrispressoParser.load_directory', **load_directory_config)


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

    ### Tests
    def test_home_assert_successful(self):
        patchers = ['discover_folders']
        self.start_patchers(patchers)

        http_response = point_mutation.views.home(self.data['get_request'])

        self.assertEqual(http_response.status_code, self.data['successful_http_response_code'])
        point_mutation.views.discover_folders.assert_called_once()

        self.stop_patchers(patchers)

    def test_discover_folders_assert_successful(self):
        patchers = ['get_dirs']
        self.start_patchers(patchers)

        discovered_folders = point_mutation.views.discover_folders(self.data['folder_path'])

        self.assertEqual(discovered_folders, 'This is a dir')
        point_mutation.discover.DiscoverFolders.get_dirs.assert_called_once_with('This is a folder path')

        self.stop_patchers(patchers)

    def test_point_mutation_view_assert_successful(self):
        patchers = ['point_mutation_summary']
        self.start_patchers(patchers)

        #http_response = point_mutation.views.point_mutation_view(self.data['session_request'], self.data['folder_path'])

        #self.assertEqual(http_response.status_code, self.data['successful_http_response_code'])
        #point_mutation.views.point_mutation_summary.assert_called_once_with('This is a folder path')

        self.stop_patchers(patchers)

    def test_point_mutation_allele_assert_successful(self): 
        patchers = ['']
        self.start_patchers(patchers)
        
        #http_response = point_mutation.views.point_mutation_allele(request, miseq, oligo_index, exp)

        #self.assertEqual(http_response, self.data['http_response'])

        self.stop_patchers(patchers)

    def test_point_mutation_upload_assert_successful(self):
        patchers = ['point_mutation_view']
        self.start_patchers(patchers)
        
        http_response = point_mutation.views.point_mutation_upload(self.data['post_request'])

        self.assertEqual(http_response.status_code, self.data['successful_http_response_code'])

        self.stop_patchers(patchers)

    def test_point_mutation_summary_assert_successful(self):
        patchers = ['load_directory']
        self.start_patchers(patchers)
        
        data = point_mutation.views.point_mutation_summary(self.data['folder_path'])

        point_mutation.parsers.crispresso_parser.CrispressoParser.load_directory.assert_called_once_with('This is a folder path')
        self.assertEqual(data['summary']['01']['percentages'], 'quant_data_test')

        self.stop_patchers(patchers)

    def test_point_mutation_summary_no_file_path_assert_successful(self):
        patchers = ['load_directory']
        self.start_patchers(patchers)
        
        data = point_mutation.views.point_mutation_summary('')

        point_mutation.parsers.crispresso_parser.CrispressoParser.load_directory.assert_called_once_with('/home/ubuntu/dev/miseq-standalone/testFiles/Miseq_093/')
        self.assertEqual(data['summary']['01']['percentages'], 'quant_data_test')

        self.stop_patchers(patchers)
