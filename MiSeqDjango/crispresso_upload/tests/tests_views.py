import io
import mock

from django.test import TestCase

from crispresso_upload.parsers.crispresso_parser import CrispressoParser

class ViewsTestCase(TestCase):
    parser = CrispressoParser()
    test_io_string = ''
    test_tar_file
    test_upload_path

    def setUp(self):
        self.test_io_string = io.StringIO('''Quantification of editing frequency:
	- Unmodified:32743 reads
	- NHEJ:92407 reads (14293 reads with insertions, 72245 reads with deletions, 7969 reads with substitutions)
	- HDR:0 reads (0 reads with insertions, 0 reads with deletions, 0 reads with substitutions)
	- Mixed HDR-NHEJ:0 reads (0 reads with insertions, 0 reads with deletions, 0 reads with substitutions)

Total Aligned:125150 reads ''')

    def test_get_quant_data_returns_populated_object(self):
        data = {}

        data = self.parser.get_quant_data(self.test_io_string)

        self.assertEqual(data['unmod'], "32743")
        self.assertEqual(data['nhej'], "92407")
        self.assertEqual(data['hdr'], "0")
        self.assertEqual(data['mix'], "0")
        self.assertEqual(data['total'], "125150")

    def test_load_tar_file_returns_true_if_file_opened(self):
        
        with mock.patch("CrispressoParser.chunkify_tar_file", self.return_true):
            self.parser.load_tar_file(test_tar_file, test_upload_path)


        with file.open(uploaded_file_path, 'r|*') as tar:
            return self.chunkify_tar_file(tar)


    def return_true(*args, **kwargs):
        return true
