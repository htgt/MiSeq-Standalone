import os
from django.test import SimpleTestCase

from unittest.mock import MagicMock, patch

import point_mutation.views


class ViewsTestCase(SimpleTestCase):
    data = None
    parser = None
    patchers = {}

    ### setup methods
    def setUp(self):
        self.data = {
            'http_response' : 'httpResponse',
            'request' : 'Request'
        }

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

    def test_home_assert_successful(self):
        patchers = ['']
        self.start_patchers(patchers)

        http_response = point_mutation.views.home(self.data['request'])

        self.assertEqual(http_response, self.data['http_response'])

        self.stop_patchers(patchers)

    def test_discover_folders_assert_successful(self):
        patchers = ['']
        self.start_patchers(patchers)

        discovered_folders = point_mutation.views.discover_folders(self.data['folder_path'])

        self.assertEqual(discovered_folders, self.data['folders_to_discover'])

        self.stop_patchers(patchers)

    def test_point_mutation_view_assert_successful(self):
        patchers = ['']
        self.start_patchers(patchers)

        http_response = point_mutation.views.point_mutation_view(self.data['request'], self.data['file_path'])

        self.assertEqual(http_response, self.data['http_response'])

        self.stop_patchers(patchers)

    def test_point_mutation_allele_assert_successful(self): 
        patchers = ['']
        self.start_patchers(patchers)
        
        http_response = point_mutation.views.point_mutation_allele(request, miseq, oligo_index, exp)

        self.assertEqual(http_response, self.data['http_response'])

        self.stop_patchers(patchers)

    def test_point_mutation_upload_assert_successful(self):
        patchers = ['']
        self.start_patchers(patchers)
        
        http_response = point_mutation.views.point_mutation_upload(self.data['request'])

        self.assertEqual(http_response, self.data['http_response'])

        self.stop_patchers(patchers)

    def test_point_mutation_summary_assert_successful(self):
        patchers = ['']
        self.start_patchers(patchers)
        
        http_response = point_mutation.views.point_mutation_summary(self.data['request'])

        self.assertEqual(http_response, self.data['http_response'])

        self.stop_patchers(patchers)
