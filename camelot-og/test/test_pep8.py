import unittest
import os
import pep8

# Using test_locations until we can just check the base path.
test_locations = [
    'setup.py',
    'fabfile.py',
]


class TestCodeFormatting(unittest.TestCase):

    '''
    Test that all code within the jets module conforms to the pep8 standard.
    '''

    def setUp(self):
        cur_dir = os.path.dirname(__file__)
        self.jets_dir = os.path.abspath(os.path.join(
            cur_dir, os.pardir))
        self.config_file = os.path.join(cur_dir, 'pep8_config')

    def _conformance(self, path):
        path = path.split('/')
        test_dir = os.path.join(
            self.jets_dir, *path)
        pep8_style = pep8.StyleGuide(
            config_file=self.config_file, paths=[test_dir])
        result = pep8_style.check_files()
        self.assertEqual(
            result.total_errors, 0,
            'Found %d code style errors/warnings in: %s!' % (
                result.total_errors, test_dir))

    def test_paths_pep8_conformance(self):
        for path in test_locations:
            self._conformance(path)

    def test_tng_pep8_conformance(self):
        self._conformance('camelot')
